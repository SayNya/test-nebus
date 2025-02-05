from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ("get_activity_tree_ids",)


async def get_activity_tree_ids(session: AsyncSession, activity_name: str) -> list[int]:
    recursive_cte = text(
        """
            WITH RECURSIVE activity_tree AS (
                SELECT id FROM activity WHERE name = :activity_name
                UNION ALL
                SELECT a.id FROM activity a
                INNER JOIN activity_tree at ON a.parent_id = at.id
            )
            SELECT id FROM activity_tree;
        """
    )

    activities = (
        await session.execute(recursive_cte, {"activity_name": activity_name})
    ).fetchall()
    if not activities:
        return []

    return [row.id for row in activities]
