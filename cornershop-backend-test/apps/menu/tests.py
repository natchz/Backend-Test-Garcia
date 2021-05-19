from django.test import TestCase
from datetime import datetime, timedelta
from apps.menu.models import Menu, Dish
from apps.employee.models import Employee
from apps.order.models import Order

class AnimalTestCase(TestCase):
    """
    Unit testing of the information storage process
    """
    def setUp(self):
        self.date = datetime.now() + timedelta(hours=24)

        Employee.objects.create(
            first_name="Luis",
            last_name="Garcia",
            country="CL",
            slack_id="#NONE"
        )

        Dish.objects.create(name="Duck a l'Orange", type=1)
        Dish.objects.create(name="Juicy Baked Pork Chops", type=1)
        Dish.objects.create(name="Olivier salad", type=2)
        Dish.objects.create(name="Cheesecake", type=3)

        dishes = Dish.objects.all()
        menu = Menu.objects.create(date=self.date, country="CL")
        menu.dishes.set(dishes)

    def test_create_menu(self):
        """
        It is verified that the menu has been created correctly
        """
        menu = Menu.objects.get(date=self.date, country="CL")

        dishes = Dish.objects.all()

        self.assertEqual(menu.is_published(), False)
        self.assertEqual(menu.dishes.count(), dishes.count())

    def test_menu_publish(self):
        """
        It is verified that the publication of the menu works correctly and
        creates the corresponding unique orders
        """
        menu = Menu.objects.get(date=self.date, country="CL")
        menu.set_publish()

        orders = menu.orders.all()

        self.assertEqual(menu.is_published(), True)
        self.assertEqual(orders.count(), 1)

    def test_make_order(self):
        """
        It is verified that an order can be placed and the quantity of
        selected dishes corresponds
        """
        menu = Menu.objects.get(date=self.date, country="CL")
        employee = Employee.objects.get(slack_id="#NONE") 

        order = Order.objects.create(
            employee=employee,
            menu=menu,
            note="Extra cheese please"
        )

        main_course = Dish.objects.get(name="Duck a l'Orange", type=1)
        salad = Dish.objects.get(name="Olivier salad", type=2)
        dessert = Dish.objects.get(name="Cheesecake", type=3)

        order.dishes.add(main_course)
        order.dishes.add(salad)
        order.dishes.add(dessert)

        self.assertEqual(order.note, "Extra cheese please")
        self.assertEqual(order.dishes.count(), 3)