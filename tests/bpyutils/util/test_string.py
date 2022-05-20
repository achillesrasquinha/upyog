import pytest

# imports - module imports
from bpyutils.util.string import (strip, strip_ansi, pluralize, kebab_case,
    safe_encode, safe_decode, upper, lower, capitalize,
    ellipsis, get_random_str, check_url, nl, tb, sanitize_html, sanitize_text)
from bpyutils import cli

def test_strip():
    string = "foobar"
    assert strip(string) == string

    string = "\n   foobar\nfoobar   \n   "
    assert strip(string) == "foobar\nfoobar"

    string = "\n\n\n"
    assert strip(string) == ""

def test_strip_ansi():
    assert strip_ansi(cli.format("foobar", cli.GREEN)) == "foobar"
    assert strip_ansi(cli.format("barfoo", cli.BOLD))  == "barfoo"

def test_pluralize():
    assert pluralize("package",  1) == "package"
    assert pluralize("package",  2) == "packages"
    assert pluralize("packages", 2) == "packages"

def test_kebab_case():
    assert kebab_case("foo bar") == "foo-bar"
    assert kebab_case("Foo Bar") == "foo-bar"
    assert kebab_case("FOO BAR") == "foo-bar"

    assert kebab_case("_FOO_BAR_", delimiter = "_") == "foo-bar"
    assert kebab_case("foo_bar",   delimiter = "_") == "foo-bar"

def test_safe_encode():
    assert safe_encode(b"foobar") == b"foobar"
    assert safe_encode( "foobar") == b"foobar"

    assert safe_encode(123456789) == 123456789

def test_safe_decode():
    assert safe_decode(b"foobar") == "foobar"
    assert safe_decode( "foobar") == "foobar"
    
    assert safe_decode(123456789) == 123456789

def test_upper():
    assert upper('foobar') == 'FOOBAR'
    assert upper('FOOBAR') == 'FOOBAR'
    assert upper('FoObAr') == 'FOOBAR'

def test_lower():
    assert lower('FoObAr') == 'foobar'
    assert lower('FOOBAR') == 'foobar'
    assert lower('foobar') == 'foobar'

def test_capitalize():
    assert capitalize('FoObAr') == 'Foobar'
    assert capitalize('FOOBAR') == 'Foobar'
    assert capitalize('foobar') == 'Foobar'

def test_ellipsis():
    sentence = 'The quick brown fox jumps over the lazy dog and humpty dumpty sat on a wall'
    assert ellipsis(sentence) == 'The quick brown fox jumps over the lazy dog and humpt...'

    assert ellipsis(sentence, threshold = 3) == 'The qu...'
    assert ellipsis(sentence, threshold = 7) == 'The quick ...'

    assert ellipsis(sentence, 100) == sentence

def test_sanitize_html():
    assert sanitize_html('<div>Hello, World!</div>') == 'Hello, World!'
    assert sanitize_html('<span><div><foo>1</foo></div></span>') == '1'

    assert sanitize_html('foobar') == 'foobar'

def test_sanitize_text():
    assert sanitize_text('&nbsp;     Hello, World!&nbsp;&nbsp;&nbsp;&nbsp;') == 'Hello, World!'
    assert sanitize_text('Hello, World!') == 'Hello, World!'

def test_get_random_str():
    assert len(get_random_str()) == 32

def test_check_url():
    correct_urls = [
        "https://google.com",
        "http://facebook.com",
        "postgres://username:password@example.com:5432/db"
    ]

    for url in correct_urls:
        assert check_url(url)
    
    incorrect_urls = [
        'goober',
        '123456789',
        "www.google.com",
        12345
    ]

    for url in incorrect_urls:
        assert not check_url(url, raise_err = False)

        with pytest.raises(ValueError):
            check_url(url)

def test_nl():
    assert nl() == "\n"
    assert nl(space = 10) == "\n\n\n\n\n\n\n\n\n\n"
    assert nl('foobar') == "foobar\n"

def test_tb():
    assert tb() == '  '
    assert tb(point = 4) == '    '
    assert tb('foobar') == '  foobar'