from pathlib import Path

package_root = Path(__file__).resolve(strict=True).parents[2]
source_dir = (package_root / "src" / "cake_bake_app").resolve(strict=True)
templates_dir = source_dir / "templates"
