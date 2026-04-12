set shell := ["powershell.exe", "-c"]

version := `taplo get -f pyproject.toml project.version`
name := `taplo get -f pyproject.toml project.name`
os_name := os()

alias help := default

# Print this message
default:
    @just --list

# Debug project info
[group("Debug")]
info:
    @echo "=== Project Info ==="
    @echo "Name: {{ name }}"
    @echo "Version: {{ version }}"
    @echo "OS: {{ os_name }}"

# Build the binary
[group("Release")]
build: info
    uv run pyinstaller -F --specpath specs -n {{ name }}-v{{ version }}-{{ os_name }} app.py
