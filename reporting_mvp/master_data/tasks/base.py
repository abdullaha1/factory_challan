"""Base task model
"""

from dramatiq.actor import Actor
from django.db import transaction
from dramatiq.message import Message
from dramatiq.broker import get_broker
from dramatiq.logging import get_logger
# from raven.contrib.django.raven_compat.models import client
# from spekit import utils
# from spekit.api.models.tasks import Tasks
# from spekit.api.email.mandrill import MandrillMailer
from utils import helper
from master_data.models import Job


class BaseActor(Actor):
    """Custom base class for our actors.
    """

    actor_name = None
    failure_template = None
    success_template = None
    task = None

    def __init__(self, broker=None, queue_name="spekit", priority=100, **options):
        """Initializer.

        :param broker: The broker object. Defaults to None, in which case
        the default broker is used.
        :param queue_name: The name of the queue. Defaults to 'default'. Very
        original, I know.
        :param priority: The job priority. Defaults to 100. Lower is higher.
        :param options: Other options.
        """
        if not self.actor_name:
            raise NotImplementedError()
        self.logger = get_logger(self.__module__, self.actor_name)
        self.broker = broker if broker else get_broker()
        self.queue_name = queue_name
        self.priority = priority
        self.options = options
        self.broker.declare_actor(self)

    def message_with_options(self, *, args=None, kwargs=None, message_id=None, **options):
        """Build a message with an arbitray set of processing options.
        This method is useful if you want to compose actors.  See the
        actor composition documentation for details.

        Parameters:
          args(tuple): Positional arguments that are passed to the actor.
          kwargs(dict): Keyword arguments that are passed to the actor.
          \**options(dict): Arbitrary options that are passed to the
            broker and any registered middleware.

        Returns:
          Message: A message that can be enqueued on a broker.
        """
        for name in ["on_failure", "on_success"]:
            callback = options.get(name)
            if isinstance(callback, Actor):
                options[name] = callback.actor_name

            elif not isinstance(callback, (type(None), str)):
                raise TypeError(name + " value must be an Actor")

        return Message(
            queue_name=self.queue_name,
            actor_name=self.actor_name,
            args=args, kwargs=kwargs or {},
            options=options, message_id=message_id or helper.generate_uuid()
        )

    def send(self, user_id, *, args=None, kwargs=None, delay=None, **options):
        """Asynchronously send a message to this actor, along with an
        arbitrary set of processing options for the broker and
        middleware.

        Parameters:
          user_id: The ID of the user creating this task.
          args(tuple): Positional arguments that are passed to the actor.
          kwargs(dict): Keyword arguments that are passed to the actor.
          delay(int): The minimum amount of time, in milliseconds, the
            message should be delayed by.
          \**options(dict): Arbitrary options that are passed to the
            broker and any registered middleware.

        Returns:
          Message: The enqueued message.
        """
        message_id = helper.generate_uuid()
        args = args or ()
        args = (message_id, ) + args
        message = self.message_with_options(
            args=args, kwargs=kwargs, message_id=message_id, **options
        )
        task = self.create_task(user_id, message.message_id, args=args, kwargs=kwargs)
        return self.broker.enqueue(message, delay=delay,)

    def create_task(self, user_id, message_id, *, args=None, kwargs=None):
        """Creates a task object for the current job.

        :param user_id: The ID of the user creating this task
        :param message_id: The ID of the message
        args(tuple): Positional arguments that are passed to the actor.
        kwargs(dict): Keyword arguments that are passed to the actor.
        """
        task = Job.objects.create(
            job_id=message_id,
            status="queued",
            type=self.actor_name,
            created_by_id=str(user_id),
            updated_by_id=str(user_id),
            data={"args": args, "kwargs": kwargs}
        )
        return task

    def instrument_task_start(self, *args, **kwargs):
        """Instrumentation that should be triggered when a task starts.
        """
        pass

    def instrument_task_end(self, *args, **kwargs):
        """Instrumentation that should be triggered when a task ends.
        """
        pass

    def instrument_task_fail(self, *args, **kwargs):
        """Instrumentation that should be triggered when a task fails.
        """
        pass

    def set_processing(self, message_id):
        """Sets the status of the current task to 'processing'.

        :param message_id: The ID of the message
        """
        Job.objects.filter(job_id=message_id).update(status="processing")
        self.instrument_task_start(message_id)

    def set_completed(self, message_id):
        Job.objects.filter(job_id=message_id).update(status="processed")

    # def send_email(self, recipients, template_name, merge_vars):
    #     """Wrapper for sending emails.
    #
    #     Handles exceptions/errors from Mandrill
    #     :param recipients: A list of objects of the following form:
    #     {
    #         "name": "Recipient",
    #         "email": "recipient@receivingdoma.in"
    #     }
    #     :param template_name: The name of the template to send
    #     :param merge_vars: The merge vars to send
    #     """
    #     response = None
    #     try:
    #         response = MandrillMailer.send_email(
    #             recipients, template_name, merge_vars
    #         )
    #     except Exception as e:
    #         self.logger.exception(e)
    #     return response

    # def set_failed(self, exception):
    #     """Sets the status of the current task to 'failed'.
    #
    #     :param exception: The exception that was caught
    #     """
    #     client.captureException()
    #     self.task.status = "failed"
    #     self.task.save()
    #     if self.failure_template:
    #         name = []
    #         if self.task.created_by.first_name and len(self.task.created_by.first_name.strip()) > 0:
    #             name.append(self.task.created_by.first_name.strip())
    #         if self.task.created_by.last_name and len(self.task.created_by.last_name.strip()) > 0:
    #             name.append(self.task.created_by.last_name.strip())
    #         name = " ".join(name)
    #         response = self.send_email([{
    #             "name": name,
    #             "email": self.task.created_by.email
    #         }], self.failure_template, [{
    #             "rcpt": self.task.created_by.email,
    #             "vars": [{
    #                 "name": "RECIPIENT",
    #                 "content": self.task.created_by.first_name
    #             }]
    #         }])
    #         if not response:
    #             self.logger.error(f"Could not set sync success email to {name}, {self.task.created_by.email}")
    #         else:
    #             for item in response:
    #                 if item["status"] in ("rejected", "invalid"):
    #                     self.logger.error(f"Email rejected with reason: {item['reject_reason']}")
    #             # self.logger.info(f"Job Failure email sent to {name}, {self.task.created_by.email}")
    #     self.instrument_task_fail(error=str(exception))
    #
    # def set_completed(self):
    #     """Sets the status of the current task to 'completed'.
    #     """
    #     self.task.status = "completed"
    #     self.task.save()
    #     if self.success_template:
    #         name = []
    #         if self.task.created_by.first_name and len(self.task.created_by.first_name.strip()) > 0:
    #             name.append(self.task.created_by.first_name.strip())
    #         if self.task.created_by.last_name and len(self.task.created_by.last_name.strip()) > 0:
    #             name.append(self.task.created_by.last_name.strip())
    #         name = " ".join(name)
    #         response = self.send_email([{
    #             "name": name,
    #             "email": self.task.created_by.email
    #         }], self.success_template, [{
    #             "rcpt": self.task.created_by.email,
    #             "vars": [{
    #                 "name": "RECIPIENT",
    #                 "content": self.task.created_by.first_name
    #             }]
    #         }])
    #         if not response:
    #             self.logger.error(f"Could not set sync success email to {name}, {self.task.created_by.email}")
    #         else:
    #             for item in response:
    #                 if item["status"] in ("rejected", "invalid"):
    #                     self.logger.error(f"Email rejected with reason: {item['reject_reason']}")
    #             # self.logger.info(f"Job Success email sent to {name}, {self.task.created_by.email}")
    #     self.instrument_task_end()

    def perform(self, *args, **kwargs):
        """The actual action to be performed.

        This method is already wrapped inside a try/except, so any handled
        exceptions should be re-raised (or other ones raised in their stead) so
        that the task can be failed gracefully.
        """
        raise NotImplementedError()

    def fn(self, message_id, *args, **kwargs):
        """Performs the task.

        :param message_id: The message ID from the queue.
        """
        self.set_processing(message_id)
        result = None
        self.task = Job.objects.get(job_id=message_id)
        try:
            with transaction.atomic():
                result = self.perform(
                    *args, **kwargs, initiator=self.task.created_by,
                )
            self.set_completed(message_id)
        except Exception as e:
            self.logger.exception(e)
            # self.set_failed(e)
        return result

    def __repr__(self):
        return f"Actor(queue_name={self.queue_name}, actor_name={self.actor_name})"
