import os
from celery import shared_task

@shared_task
def send_slack_notifications(pk):
    """
    Task for the creation of unique orders for each employee and the
    subsequent notification of these by private message to their
    slack user
    """

    import uuid
    from itertools import islice
    from apps.menu.models import Menu
    from apps.employee.models import Employee
    from apps.order.models import Order
    from backend_test.utils.slack import SlackClient

    menu_object = Menu.objects.get(pk=pk)
    employees = Employee.objects.filter(country=menu_object.country)

    # Will be taken into account to create the orders inthe database
    batch_size = 25
    # Stores in memory a lunch order for each employee in the country
    orders = (
        Order(
            id=uuid.uuid4(), menu=menu_object, employee=employee
        ) for employee in employees
    )

    """
    Slack client with singleton implementation, it will only take time
    with the first call
    """
    slack_client = SlackClient()

    # While there are still orders to create
    while True:
        """
        A maximum of "batch_size" of orders are extracted for their
        creation
        """
        batch = list(islice(orders, batch_size))
        if not batch:
            # There are no more orders to create
            break

        Order.objects.bulk_create(batch, batch_size)

        for order in batch:
            try:
                """
                A private message is sent to each employee with the
                menu link
                """
                slack_client.send_user_message(
                    order.employee.slack_id,
                    "Hi %s, Cornerlunch has already published the '%s', you can use the following link to place your order: %s" % (
                        order.employee.get_short_name(),
                        str(menu_object),
                        "https://nora.cornershop.io/menu/%s" % (order.id)
                    )
                )
            except Exception as e:
                """
                The order must be marked for further processing through a
                calendar task
                """
                pass