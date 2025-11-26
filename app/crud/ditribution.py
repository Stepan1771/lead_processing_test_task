import random

from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models.contact import Contact
from core.models.operator import Operator

from .operators import crud_operators
from .contacts import crud_contacts


class DistributionService:
    """
    Сервис для распределения лидов между операторами.
    """


    @staticmethod
    async def find_best_operator(
            source_id: int,
            current_operators: List[Operator]
    ) -> Optional[Operator]:
        """
        Найти лучшего оператора для данного источника.

        Args:
            source_id: ID источника
            current_operators: Список доступных операторов

        Returns:
            Optional[Operator]: Лучший оператор или None
        """
        try:
            if not current_operators:
                HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Available operators not found",
                )

            source_id_str = str(source_id)
            operators_with_weights = []

            for op in current_operators:
                # Получаем вес компетенции для данного источника
                weight = op.competencies.get(source_id_str, 1.0)

                # Рассчитываем приоритет на основе компетенции и текущей нагрузки
                available_capacity = op.max_load_limit - op.current_load
                priority = weight * available_capacity
                operators_with_weights.append((op, priority))

            # Если есть операторы с компетенциями, выбираем по весам
            competent_operators = [op for op, priority in operators_with_weights if priority > 0]

            rand_val = None

            if competent_operators:
                # Взвешенный случайный выбор
                total_priority = sum(priority for _, priority in operators_with_weights)
                if total_priority > 0:
                    rand_val = random.uniform(0, total_priority)
                cumulative = 0
                for op, priority in operators_with_weights:
                    cumulative += priority
                    if rand_val <= cumulative:
                        return op

            # Если нет операторов с компетенциями, выбираем случайно из доступных
            result = random.choice(current_operators) if current_operators else None
            return result

        except Exception as e:
            raise e


    @staticmethod
    async def distribute_contact(
            session: AsyncSession,
            contact: Contact
    ) -> Optional[Operator]:
        """
        Распределить обращение на оператора.

        Args:
            session: AsyncSession Сессия БД
            contact: Обращение для распределения

        Returns:
            Optional[Operator]: Назначенный оператор или None
        """
        try:
            # Получаем активных операторов с доступной емкостью
            available_operators = await crud_operators.get_active_operators(
                session=session,
            )

            if not available_operators:
                HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Available operators not found",
                )

            # Находим лучшего оператора
            best_operator = await DistributionService.find_best_operator(
                contact.source_id, available_operators
            )

            if best_operator:
                # Назначаем оператора на обращение
                await crud_contacts.assign_operator(session, contact.id, best_operator.id)
                # Увеличиваем нагрузку оператора
                await crud_operators.update_load(session, best_operator.id, 1)

                return best_operator

            return None

        except Exception as e:
            raise e

    @staticmethod
    async def distribute_all_undistributed(session: AsyncSession) -> List[dict]:
        """
        Распределить все нераспределенные обращения.

        Args:
            session: AsyncSession: Сессия БД

        Returns:
            List[dict]: Результаты распределения
        """
        try:
            undistributed_contacts = await crud_contacts.get_undistributed(session)
            results = []

            for contact in undistributed_contacts:
                operator = await DistributionService.distribute_contact(session, contact)
                results.append({
                    "contact_id": contact.id,
                    "lead_id": contact.lead_id,
                    "source_id": contact.source_id,
                    "assigned_operator_id": operator.id if operator else None,
                    "success": operator is not None
                })

            return results

        except Exception as e:
            raise e



distribution_service = DistributionService()