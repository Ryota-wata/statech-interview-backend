from sqlalchemy.orm.session import Session

# スキーマ
from api.schemas.response_model.result import ResultResponseModel

# use_case基底クラス
from api.use_cases.base import UseCaseBaseModel

# repositoryクラス
from api.repository.result import ResultCrudRepository


class CrudReslut(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session

    async def register_reslut(self, user_id: str, corporate_id: int, quiz_result: bool) -> None:
        """クイズ結果を保存

        ユーザーのクイズに対する結果を保存

        """

        await ResultCrudRepository(session=self.session).register_result(user_id=user_id, corporate_id=corporate_id, quiz_result=quiz_result)

        return None
