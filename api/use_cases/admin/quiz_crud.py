from sqlalchemy.orm.session import Session

# スキーマ
from api.schemas.response_model.quiz_crud import QuizResponseModel

# use_case基底クラス
from api.use_cases.base import UseCaseBaseModel

# repositoryクラス
from api.repository.admin.quiz_crud import QuizRepository


class QuizCrud(UseCaseBaseModel):
    def __init__(self, session: Session):
        self.session = session


    async def get_quizzes_all(self) -> list[QuizResponseModel]:
        """クイズを全て取得"""

        quizzes = await QuizRepository(session=self.session).fetch_quizzes()

        return quizzes
    

    async def create_quiz(self, create_quiz):
        """クイズ新規作成"""

        new_quiz = await QuizRepository(session=self.session).store_quiz(create_quiz=create_quiz)

        return new_quiz
    
    
    async def update_quiz(self, question_id, update_quiz):
        """クイズ編集"""

        update_quiz = await QuizRepository(session=self.session).update_quiz(question_id=question_id, update_quiz=update_quiz)

        return update_quiz
    
    
    async def delete_quiz(self, question_id):
        """クイズ削除"""

        await QuizRepository(session=self.session).delete_quiz(question_id=question_id)
