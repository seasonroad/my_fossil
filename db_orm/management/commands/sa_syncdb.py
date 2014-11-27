# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from db_orm import db


class Command(NoArgsCommand):
    help = 'Create all tables used in project'

    def handle_noargs(self, **options):
        try:
            engine = db.session.get_bind()
            db.metadata.create_all(engine)
        except Exception as exc:
            print exc
