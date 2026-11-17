from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import models
import schemas
from router.auth import get_current_user
from database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def _get_owned_transaction(
    db: Session, transaction_id: int, user: models.User
) -> models.Transaction:
    """Fetch a transaction only if it belongs to `user`.

    Returns 404 both when it doesn't exist and when it belongs to someone else,
    so we never leak whether another user's transaction exists.
    """
    transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == user.id,
        )
        .first()
    )
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found",
        )
    return transaction


@router.post(
    "",
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_transaction = models.Transaction(
        **transaction.model_dump(), owner_id=current_user.id
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@router.get("", response_model=List[schemas.TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.owner_id == current_user.id)
        .all()
    )


# NOTE: /filter MUST be declared before /{transaction_id}, otherwise FastAPI
# would try to parse the word "filter" as an integer id and return 422.
@router.get("/filter", response_model=List[schemas.TransactionResponse])
def filter_transactions(
    type: Optional[Literal["income", "expense"]] = Query(None, examples=["expense"]),
    category: Optional[str] = Query(None, examples=["Food"]),
    minimum_amount: Optional[float] = Query(None, ge=0, examples=[100]),
    maximum_amount: Optional[float] = Query(None, ge=0, examples=[5000]),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if (
        minimum_amount is not None
        and maximum_amount is not None
        and minimum_amount > maximum_amount
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="minimum_amount cannot be greater than maximum_amount",
        )

    query = db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    )
    if type is not None:
        query = query.filter(models.Transaction.type == type)
    if category is not None:
        query = query.filter(models.Transaction.category.ilike(category))
    if minimum_amount is not None:
        query = query.filter(models.Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(models.Transaction.amount <= maximum_amount)
    return query.all()


@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return _get_owned_transaction(db, transaction_id, current_user)


@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    updates: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = _get_owned_transaction(db, transaction_id, current_user)

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = _get_owned_transaction(db, transaction_id, current_user)
    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction {transaction_id} deleted successfully"}
