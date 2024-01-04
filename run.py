# 1 Создать двух пользователей (с помощью метода User.objects.create_user('username')).
User.objects.create_user('user1')
User.objects.create_user('user2')

# 2 Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(user=User.objects.get(username='user1'))
Author.objects.create(user=User.objects.get(username='user2'))

# 3 Добавить 4 категории в модель Category.
Category.objects.create(category='спорт')
Category.objects.create(category='политика')
Category.objects.create(category='образование')
Category.objects.create(category='биография')
Category.objects.create(category='здоровье')

# 4 Добавить 2 статьи и 1 новость.
Post.objects.create(post='A', user=Author.objects.all()[0], title='О статьях', text='Короткая статья — не более чем короткая статья, её единственное отличие от остальных заключается в её размере, будь то 2—3 или даже 5 предложений или строк.')
Post.objects.create(post='A', user=Author.objects.all()[0], title='Статья «Интернет — средство омоложения»', text='Если раньше считалось, что сеть разрушает здоровье, то теперь дозы интернета прописывают пожилым американским пациентам как панацею от раннего старения и как профилактику инсультов, а также старческого слабоумия.')
Post.objects.create(post='N', user=Author.objects.all()[1], title='Лица проекта. Сигнал судьбы', text='Победительница столичного конкурса «СуперБабушка-2013» Раиса Оленина одной из первых заполнила анкету участника проекта «Московское долголетие» и сейчас занимается в нескольких кружках. Она награждена дипломом лауреата премии «Человек года 2019» в номинации «За верность проекту». И накануне своего 80-летнего юбилея готова к новому повороту.')

# 5 Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
Post.objects.get(id=1).categories.add(Category.objects.get(id=3))
Post.objects.get(id=2).categories.add(Category.objects.get(id=3)) 
Post.objects.get(id=2).categories.add(Category.objects.get(id=5))
Post.objects.get(id=3).categories.add(Category.objects.get(id=4)) 

 
# 6 Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть 
#    как минимум один комментарий).
Comment.objects.create(post=Post.objects.get(id=1), user=User.objects.get(username='user2'), text='Статья ни о чём')
Comment.objects.create(post=Post.objects.get(id=2), user=User.objects.get(username='user2'), text='Интерессное лекарство')
Comment.objects.create(post=Post.objects.get(id=2), user=User.objects.get(username='user1'), text='И полечился и отвлёкся')
Comment.objects.create(post=Post.objects.get(id=3), user=User.objects.get(username='user1'), text='Мощная бабушка')

# 7 Применяя функции like() и dislike() к статьям/новостям и комментариям, 
# скорректировать рейтинги этих объектов. 

Comment.objects.get(id=1).dislike()
Comment.objects.get(id=2).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=4).like()
Comment.objects.get(id=4).like()

Post.objects.get(id=1).dislike()
Post.objects.get(id=2).like()
Post.objects.get(id=3).like()
Post.objects.get(id=3).like()

# 8 Обновить рейтинги пользователей.
User.objects.get(pk=1).author.update_rating()
User.objects.get(pk=2).author.update_rating()

# 9 Вывести username и рейтинг лучшего пользователя 
# (применяя сортировку и возвращая поля первого объекта).
User.objects.order_by('-author__rating_user').first().username

# 10 Вывести дату добавления, username автора, рейтинг, 
# заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
Post.objects.order_by('-rating_new').first().date_added
Post.objects.order_by('-rating_new').first().user.user
Post.objects.order_by('-rating_new').first().rating_new
Post.objects.order_by('-rating_new').first().title
Post.objects.order_by('-rating_new').first().preview()

# 11 Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=Post.objects.order_by('-rating_new').first()).values_list('date_added', 'user__author__user__username', 'rating_comment', 'text')