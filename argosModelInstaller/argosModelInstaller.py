import argostranslate.package

def checkModel(from_code="fr", to_code="en"):
    installed_packages = argostranslate.package.get_installed_packages()
    for pkg in installed_packages:
        if pkg.from_code == from_code and pkg.to_code == to_code:
            return True

    try:
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()

        package_to_install = next(
            (p for p in available_packages if p.from_code == from_code and p.to_code == to_code),
            None
        )

        if not package_to_install:
            return False

        argostranslate.package.install_from_path(package_to_install.download())
        return True

    except Exception:
        return False
