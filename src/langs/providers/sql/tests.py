# -*- coding: utf-8 -*-
from django.test import TestCase
from src.langs.models import Lang
from src.tasks.models import Task
from src.training.models.taskitem import Solution
from src.utils.db import load_dump, remove_db_objects

class ProviderTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('===> reset db')
        remove_db_objects()  #удаление базы данных
        load_dump()          #загрузка dump-а

    def test_provider(self):

        """ Прогон sql по тестовой выборке задач """

        print('===> RUN Sql tests')
        provider = Lang.objects.get(provider_name=langs.SQL).provider    #получение класса Provider для модуля sql
        # Задачи, тесты которых должны закончиться успехом
        for task in Task.objects.filter(lang=langs.SQL, tags__name='success'):   #получение заданий, которые должны выполниться успешно
            solution = task.solution_examples.filter(lang=langs.SQL).first()    #Получение эталонного решения
            tests_result = provider.check_tests(content=solution.content, task=task) #отправка теста на проверку
            self.assertTrue(
                expr=tests_result['success'],
                msg=f'id={task.id}, title="{task.title}"'
            )
            print(f'===> SUCCESS: {task}')

        # Задачи, тесты которых должны провалиться
        for task in Task.objects.filter(lang=langs.SQL, tags__name='unluck'):
            solution = task.solution_examples.filter(lang=langs.SQL).first()
            tests_result = provider.check_tests(content=solution.content, task=task)
            self.assertFalse(
                expr=tests_result['success'],
                msg=f'id={task.id}, title="{task.title}"'
            )
            print(f'===> UNLUCK: {task}')
