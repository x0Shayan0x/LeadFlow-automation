import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.lead import Lead
from app.schemas.lead import LeadRead, LeadUpsert, LeadUpsertResponse


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/leads",
    tags=["Leads"],
)


@router.post(
    "",
    response_model=LeadUpsertResponse,
    responses={
        200: {"description": "Existing lead updated"},
        201: {"description": "New lead created"},
    },
)
async def upsert_lead(
    payload: LeadUpsert,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> LeadUpsertResponse:
    insert_statement = insert(Lead).values(
        **payload.model_dump(),
    )

    upsert_statement = insert_statement.on_conflict_do_update(
        index_elements=[Lead.email],
        set_={
            "full_name": insert_statement.excluded.full_name,
            "company": insert_statement.excluded.company,
            "role": func.coalesce(
                insert_statement.excluded.role,
                Lead.role,
            ),
            "website": func.coalesce(
                insert_statement.excluded.website,
                Lead.website,
            ),
            "source": insert_statement.excluded.source,
            "notes": func.coalesce(
                insert_statement.excluded.notes,
                Lead.notes,
            ),
            "workflow_execution_id": func.coalesce(
                insert_statement.excluded.workflow_execution_id,
                Lead.workflow_execution_id,
            ),
            "occurrence_count": Lead.occurrence_count + 1,
            "last_received_at": func.now(),
            "updated_at": func.now(),
        },
    ).returning(Lead)

    try:
        result = await session.execute(upsert_statement)
        lead = result.scalar_one()
        await session.commit()
    except SQLAlchemyError as error:
        await session.rollback()
        logger.exception("Failed to store lead.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The lead could not be stored.",
        ) from error

    operation: Literal["created", "updated"]

    if lead.occurrence_count == 1:
        operation = "created"
        response.status_code = status.HTTP_201_CREATED
    else:
        operation = "updated"
        response.status_code = status.HTTP_200_OK

    return LeadUpsertResponse(
        operation=operation,
        lead=LeadRead.model_validate(lead),
    )
