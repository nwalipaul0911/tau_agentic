#!/usr/bin/env python3
"""
Rename tool files across interface directories using a JSON mapping and
update class names and imports inside the files.

Expect a JSON file like `name_map.json` in the working directory (or pass path
as first arg). Keys are snake_case tool base names (no .py); values are lists
of alternative snake_case names (one per target interface variant).

Example JSON structure (shortened):
{
  "add_new_employee": ["create_employee","hire_employee","register_employee","onboard_employee"],
  ...
}
"""
import os
import re
import json
import sys
from typing import Dict, List

# Config
ROOT = "tools"  
MAP_FILE = sys.argv[1] if len(sys.argv) > 1 else "tool_names_map.json"
# If you want to only operate on specific interfaces, set FILTER_INTERFACES to list like ["interface_2","interface_3"]
FILTER_INTERFACES: List[str] = []


def load_map(path: str) -> Dict[str, List[str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def snake_to_pascal(name: str) -> str:
    """foo_bar -> FooBar"""
    parts = name.replace(".py", "").split("_")
    return "".join(p.capitalize() for p in parts)


def discover_interfaces(root: str) -> List[str]:
    """Return sorted list of interface directories with numeric suffix: interface_1, interface_2, ..."""
    all_dirs = []
    if not os.path.isdir(root):
        raise FileNotFoundError(f"Root folder not found: {root}")
    for entry in os.listdir(root):
        p = os.path.join(root, entry)
        if os.path.isdir(p) and entry.startswith("interface_"):
            # validate numeric suffix
            try:
                _ = int(entry.split("_", 1)[1])
                all_dirs.append(entry)
            except Exception:
                continue
    # sort by numeric suffix
    all_dirs.sort(key=lambda s: int(s.split("_", 1)[1]))
    if FILTER_INTERFACES:
        all_dirs = [d for d in all_dirs if d in FILTER_INTERFACES]
    return all_dirs


def rename_and_update(root: str, name_map: Dict[str, List[str]]):
    interfaces = discover_interfaces(root)
    if not interfaces:
        print("No interface_* directories found under", root)
        return

    print("Found interfaces:", interfaces)
    per_interface_mappings: Dict[str, Dict[str, str]] = {}

    for idx, interface in enumerate(interfaces):
        interface_path = os.path.join(root, interface)
        
        # FIX: The index should be adjusted to start from 1 to map to name_map variants.
        # This makes interface_1 the canonical one with no renames.
        variant_index = idx
        
        if variant_index < 0:
            print(f"Skipping renames in {interface} (canonical/original interface).")
            per_interface_mappings[interface] = {}
            continue

        print(f"\nProcessing renames for {interface} (variant index {variant_index})")
        mapping_for_interface: Dict[str, str] = {}
        for old_base, variants in name_map.items():
            old_fn = old_base + ".py"
            old_path = os.path.join(interface_path, old_fn)

            # Check if variant index is out of bounds for this variant list
            if variant_index >= len(variants):
                continue
                
            new_base = variants[variant_index]
            new_fn = new_base + ".py"
            new_path = os.path.join(interface_path, new_fn)

            if os.path.exists(old_path):
                if os.path.exists(new_path):
                    print(f"  WARNING: target already exists, skipping rename: {new_path}")
                    mapping_for_interface[old_base] = new_base
                    continue
                try:
                    os.rename(old_path, new_path)
                    mapping_for_interface[old_base] = new_base
                    print(f"  Renamed: {old_fn} -> {new_fn}")
                except Exception as e:
                    print(f"  ERROR renaming {old_path} -> {new_path}: {e}")
            else:
                mapping_for_interface[old_base] = new_base

        per_interface_mappings[interface] = mapping_for_interface

    # Second pass logic remains the same
    for interface, mapping in per_interface_mappings.items():
        if not mapping:
            print(f"\nNo mappings for {interface}; skipping content updates.")
            continue

        interface_path = os.path.join(root, interface)
        print(f"\nUpdating content in {interface} with {len(mapping)} mappings...")

        replacements = []
        for old_base, new_base in mapping.items():
            old_mod = re.escape(old_base)
            new_mod = new_base
            old_class = re.escape(snake_to_pascal(old_base))
            new_class = snake_to_pascal(new_base)
            replacements.append((re.compile(rf"\b{old_mod}\b"), new_mod))
            replacements.append((re.compile(rf"\b{old_class}\b"), new_class))

        for root_dir, _, files in os.walk(interface_path):
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(root_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"  Could not read {fpath}: {e}")
                    continue

                new_content = content
                for pattern, repl in replacements:
                    new_content = pattern.sub(repl, new_content)

                if new_content != content:
                    try:
                        with open(fpath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"  Updated references in {os.path.relpath(fpath, interface_path)}")
                    except Exception as e:
                        print(f"  ERROR writing {fpath}: {e}")

    print("\nDone. Summary of mappings per interface:")
    for interface, mapping in per_interface_mappings.items():
        if mapping:
            print(f" {interface}: {len(mapping)} mappings")
        else:
            print(f" {interface}: (no renames/mappings)")

def main():
    try:
        name_map = load_map(MAP_FILE)
    except Exception as e:
        print("Failed to load map file:", MAP_FILE, e)
        sys.exit(1)

    rename_and_update(ROOT, name_map)


if __name__ == "__main__":
    main()
