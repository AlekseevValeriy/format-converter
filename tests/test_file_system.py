import pytest

from formatconverter.file_system import *


@pytest.mark.parametrize(
    "text",
    [
        [],
        ["hello world!"],
        ["first line\n", "second_line"],
        ["one\n", "two\n", "three"],
        [(["line\n"] * 999 + ["line"])[0]],
    ],
)
def test_read_file(tmp_path, text):
    test_file = tmp_path / "test_file.txt"

    with open(test_file, "w", encoding="utf-8", errors="ignore") as file:
        file.writelines(text)

    assert test_file.exists()
    assert FileSystem().read_file(test_file) == text


@pytest.mark.parametrize(
    "text",
    [
        [],
        ["hello world!"],
        ["first line\n", "second_line"],
        ["one\n", "two\n", "three"],
        [(["line\n"] * 999 + ["line"])[0]],
    ],
)
def test_write_file(tmp_path, text):
    test_file = tmp_path / "test_file.txt"
    FileSystem().write_file(test_file, text)

    assert test_file.exists()
    with open(test_file, "r", encoding="utf-8", errors="ignore") as file:
        assert file.readlines() == text


@pytest.mark.parametrize(
    "suffix, expected_result",
    [
        ("", "test_file.txt"),
        ("a", "test_file.a"),
        ("a" * 1000, f"test_file.{'a' * 1000}"),
    ],
)
def test_add_suffix(tmp_path, suffix, expected_result):
    test_file = tmp_path / "test_file.txt"

    assert FileSystem().add_suffix(test_file, f".{suffix}").name == expected_result

@pytest.mark.parametrize(
    "text",
    [
        [],
        ["hello world!"],
        ["first line\n", "second_line"],
        ["one\n", "two\n", "three"],
        [(["line\n"] * 999 + ["line"])[0]],
    ],
)
def test_get_file_content(tmp_path, text):
    test_file = tmp_path / "test_file.txt"
    with open(test_file, "w", encoding="utf-8", errors="ignore") as file:
        file.writelines(text)
    
    content = FileSystem().get_file_content(test_file)
    
    assert test_file.exists()
    assert content == FileContent(test_file, text)


@pytest.mark.parametrize(
    "files, predicate, expected_result",
    [
        ([], lambda a: a, []),
        ([("test1.txt", ["text"])], lambda a: a, [("test1.txt", ["text"])]),
        ([
            ("test1.txt", ["text"]),
            ("test2.tx", ["text"]),
            ("test3.t", ["text"])
            ], lambda a: a, [
            ("test1.txt", ["text"]),
            ("test2.tx", ["text"]),
            ("test3.t", ["text"])
            ]), 
        ([
            ("test1.txt", ["text"]),
            ("test2.tx", ["text"]),
            ("test3.t", ["text"])
            ], lambda a: str(a).endswith("txt"), [
            ("test1.txt", ["text"])
            ]),
    ],
)
def test_get_files_content(tmp_path, files, predicate, expected_result):
    for name, text in files:
        path = tmp_path / name
        with open(path, "w", encoding="utf-8", errors="ignore") as file:
            file.writelines(text)
        assert path.exists()
            
    result = FileSystem().get_files_content(tmp_path, predicate)
    
    assert len(result) == len(expected_result)
    
    result.sort(key=lambda a: a.path.name)
    expected_result.sort(key=lambda a: a[0])
    
    for fact, expected in zip(result, expected_result):
        assert fact.path.name == expected[0]
        assert fact.content == expected[1]
