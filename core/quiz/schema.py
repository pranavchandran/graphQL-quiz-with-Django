import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes, Category, Question, Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "quiz")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")

class Query(graphene.ObjectType):
    # quiz = graphene.String()
    # all_quizzes = graphene.List(QuizzesType)
    # all_quizzes = graphene.Field(QuizzesType, id=graphene.Int())
    # import pdb ; pdb.set_trace()
    # all_questions = graphene.List(QuestionType)

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.all()

    def resolve_all_quizzes(root, info, id):
        return Quizzes.objects.get(pk=id)
    
    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)

class QuizzesMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.Int(required=True)
        delete_id = graphene.Int()

    quiz = graphene.Field(QuizzesType)

    @classmethod
    def mutate(cls, root, info, title, id, delete_id=0):
        if delete_id != 0:
            quiz = Quizzes.objects.get(id=delete_id)
            import pdb ; pdb.set_trace()
            quiz.delete()
            print(quiz)
            if quiz.id is None:
                return
            import pdb ; pdb.set_trace()
            
            # return f'Deleted {delete_id}'
        else:
            quiz = Quizzes(title=title)
            quiz.category_id = id
            # category = Category(name=name)
            quiz.save()
            return QuizzesMutation(quiz=quiz)
#fields = ("id", "title", "category", "quiz") 



class Mutation(graphene.ObjectType):
    update_category = CategoryMutation.Field()
    update_quizzes = QuizzesMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
