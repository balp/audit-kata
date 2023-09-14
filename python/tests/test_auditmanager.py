import datetime
from pathlib import Path, PurePath
from unittest.mock import MagicMock

from auditmanager import AuditManager, FileContent, FileUpdate


def test_adds_new_visitor_to_a_new_file_when_end_of_last_file_reached():
    sut = AuditManager(3)
    contents = [
        FileContent(PurePath("audit_1.txt"), []),
        FileContent(
            PurePath("audit_2.txt"),
            [
                "Peter;2019-04-06T16:30:00",
                "Jane;2019-04-06T16:40:00",
                "Jack;2019-04-06T17:00:00",
            ],
        ),
    ]
    update = sut.add_record(
        contents, "Alice", datetime.datetime.fromisoformat("2019-04-06T18:00:00")
    )
    assert update == FileUpdate(PurePath("audit_3.txt"), "Alice;2019-04-06T18:00:00")
