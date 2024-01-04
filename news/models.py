from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Модель Author
    Модель, содержащая объекты всех авторов.
    Имеет следующие поля:
        +cвязь «один к одному» с встроенной моделью пользователей User;
        +рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)
        
    def update_rating(self):
        """
        Метод update_rating() модели Author, который обновляет рейтинг текущего автора
        (метод принимает в качестве аргумента только self).
        Он состоит из следующего:
            +суммарный рейтинг каждой статьи автора умножается на 3;
            +суммарный рейтинг всех комментариев автора;
            +суммарный рейтинг всех комментариев к статьям автора.
        """ 
        self.rating_user = 0
        #суммарный рейтинг каждой статьи автора умножается на 3
        for i in self.post_set.all().values_list('rating_new'):
            self.rating_user += i[0]
        self.rating_user = self.rating_user*3
        #суммарный рейтинг всех комментариев автора
        for i in Comment.objects.filter(user=User.objects.get(username=self.user.username)).values_list('rating_comment'):
            self.rating_user += i[0]                
        #суммарный рейтинг всех комментариев к статьям автора
        for i in Post.objects.filter(user=self):
            for j in i.comment_set.all().values_list('rating_comment'):
                self.rating_user += j[0]
        self.save()                
            
        
class Category(models.Model):
    """Модель Category
    Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.). 
    Имеет единственное поле: 
        +название категории. 
    Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True)."""
    category = models.CharField(max_length=255, unique=True)    


class Post(models.Model):
    """Модель Post
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи. 
    Каждый объект может иметь одну или несколько категорий.
    Соответственно, модель должна включать следующие поля:
        +связь «один ко многим» с моделью Author;
        +поле с выбором — «статья» или «новость»;
        +автоматически добавляемая дата и время создания;
        +связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
        +заголовок статьи/новости;
        +текст статьи/новости;
        +рейтинг статьи/новости."""
    article = "A"
    news = "N"
    POST = [(article, "Статья"),
            (news, "Новость")]
    
    post = models.CharField(max_length=1,
                            choices=POST,
                            default=article)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating_new = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through="PostCategory")
    
    def like(self):
        """
        Increases the rating of the post by 1.
        """
        self.rating_new += 1
        self.save()
    
    def dislike(self):
        """
        Increases the rating of the post by -1.
        """
        self.rating_new -= 1
        self.save()
    
    def preview(self):
        """
        Returns the first 124 characters of the post with an ellipsis (...) at the end.

        Parameters:
            self (Post): The current instance of the Post model.

        Returns:
            str: The first 124 characters of the post with an ellipsis (...) at the end.
        """
        if len(self.text) <= 124:
            return self.text
        else:
            return self.text[:124] + "..."


class PostCategory(models.Model):
    """Модель PostCategory
    Промежуточная модель для связи «многие ко многим»:
        +связь «один ко многим» с моделью Post;
        +связь «один ко многим» с моделью Category."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    

class Comment(models.Model):
    """Модель Comment
    Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать 
    их способ хранения тоже.
    Модель будет иметь следующие поля:
        +связь «один ко многим» с моделью Post;
        +связь «один ко многим» со встроенной моделью User (комментарии может оставить 
                                                            любой пользователь, необязательно автор);
        +текст комментария;
        +дата и время создания комментария;
        +рейтинг комментария."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    
    def like(self):
        """
        Increases the rating of the post by 1.
        """
        self.rating_comment += 1
        self.save()
    
    def dislike(self):
        """
        Increases the rating of the post by -1.
        """
        self.rating_comment -= 1
        self.save()
