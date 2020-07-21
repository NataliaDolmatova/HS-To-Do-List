from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///card.s3db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def main_menu():
    first_option = '1) Today\'s tasks'
    second_option = '2) Week\'s tasks'
    third_option = '3) All tasks'
    fourth_option = '4) Missed tasks'
    fifth_option = '5) Add task'
    six_option = '6) Delete task'
    exit_option = '0) Exit'
    print(f"{first_option}\n{second_option}\n{third_option}\n{fourth_option}\n{fifth_option}\n{six_option}\n{exit_option}")


def user_input():
    return input('> ')


def no_tasks():
    print('Nothing to do!\n')


def today_tasks():
    today = datetime.today().date()
    print(f"Today {today.strftime('%d %b')}:")
    rows = session.query(Table).filter(Table.deadline == today).all()
    if len(rows) == 0:
        no_tasks()
    else:
        state = True
        task_number = 1
        for row in rows:
            print(f"{task_number}. {row.task}")
            task_number += 1
            state = False
        if state:
            no_tasks()
        else:
            print()


def week_tasks():
    today = datetime.today().date()
    for day in range(7):
        rows = session.query(Table).filter(Table.deadline == today).all()
        row_number = 1
        print(f"{today.strftime('%A %d %b')}:")
        if rows:
            for row in rows:
                print(f"{row_number}. {row.task}")
            print()
        else:
            no_tasks()
        today += timedelta(days=1)


def all_tasks():
    rows = session.query(Table).all()
    row_number = 1
    for row in rows:
        print(f"{row_number}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        row_number += 1
    if rows:
        print()
    else:
        print("There is no planned tasks.\n")


def add_task():
    print('Enter task')
    new_task = user_input()
    print('Enter deadline')
    task_deadline = user_input()
    date_object = datetime.strptime(task_deadline, '%Y-%m-%d')
    new_row = Table(task=new_task, deadline=date_object)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def missed_tasks():
    print('Missed tasks:')
    today = datetime.today().date()
    rows = session.query(Table).order_by(Table.deadline)
    row_number = 1
    for row in rows:
        if row.deadline == today:
            break
        print(f"{row_number}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        row_number += 1
    if rows:
        print()
    else:
        print("Nothing is missed!\n")


def delete_task():
    print('Chose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline)
    row_number = 1
    for row in rows:
        print(f"{row_number}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        row_number += 1
    choice_number = int(input())
    delete_row = rows[choice_number]
    session.delete(delete_row)
    session.commit()


def exit_menu():
    print('Bye!\n')


def processor():
    main_menu()
    choice = user_input()
    print()
    if choice == '1':
        today_tasks()
    elif choice == '2':
        week_tasks()
    elif choice == '3':
        all_tasks()
    elif choice == '4':
        missed_tasks()
    elif choice == '5':
        add_task()
    elif choice == '6':
        delete_task()
    elif choice == '0':
        exit_menu()
        return
    else:
        print('Input was incorrect.')
    processor()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    processor()