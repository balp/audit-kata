import datetime
from pathlib import Path
from unittest.mock import MagicMock

from auditmanager import AuditManager


def test_adds_new_visitor_to_a_new_file_when_end_of_last_file_reached():
    file_system_mock = MagicMock()
    file_system_mock.get_files.return_value = [
        "audits/audit_2.txt",
        "audits/audit_1.txt",
    ]
    file_system_mock.read_all_lines.return_value = [
        "Peter;2019-04-06T16:30:00",
        "Jane;2019-04-06T16:40:00",
        "Jack;2019-04-06T17:00:00",
    ]

    sut = AuditManager(3, Path("audits"), file_system_mock)
    sut.add_record("Alice", datetime.datetime.fromisoformat("2019-04-06T18:00:00"))
    file_system_mock.write_all_text.assert_called_with(
        Path("audits/audit_3.txt"), "Alice;2019-04-06T18:00:00"
    )
