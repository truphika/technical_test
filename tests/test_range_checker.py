from api.services.coverage_checker import CoverageChecker
from api.entities.point import DecimalDegreePoint


def test_close_point(site_paris, point_close):
    dataset = [site_paris]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_close)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == True
    assert orange_coverage.supports_3G == True
    assert orange_coverage.supports_4G == True


def test_point_out_of_3g_range(site_paris, point_out_3g_range):
    dataset = [site_paris]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_out_3g_range)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == True
    assert orange_coverage.supports_3G == False
    assert orange_coverage.supports_4G == True

def test_point_out_of_4g_range(site_paris, point_out_4g_range):
    dataset = [site_paris]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_out_4g_range)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == True
    assert orange_coverage.supports_3G == False
    assert orange_coverage.supports_4G == False


def test_point_out_of_range(site_paris, point_out_2g_range):
    dataset = [site_paris]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_out_2g_range)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == False
    assert orange_coverage.supports_3G == False
    assert orange_coverage.supports_4G == False

def test_point_out_of_4g_range_matched_by_second_site(site_paris, site_marseille):
    dataset = [site_marseille, site_paris]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(DecimalDegreePoint(48.752682, 2.202318))

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == True
    assert orange_coverage.supports_3G == False
    assert orange_coverage.supports_4G == False

def test_close_point_without_2g(site_paris, point_close):
    site = site_paris.copy()
    site["2G"] = 0
    dataset = [site]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_close)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == False
    assert orange_coverage.supports_3G == True
    assert orange_coverage.supports_4G == True


def test_close_point_first_point_without_2g(site_paris, point_close):
    site = site_paris.copy()
    site["2G"] = 0
    site["y"] = site["y"] - 1

    dataset = [site, site_paris]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_close)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == True
    assert orange_coverage.supports_3G == True
    assert orange_coverage.supports_4G == True

def test_close_point_wrong_operator(site_paris, site_marseille, point_close):
    site = site_paris.copy()
    site["Operateur"] = "Bouygues"

    dataset = [site_marseille, site]
    checker = CoverageChecker(dataset)
    all_coverage = checker.get_point_coverage(point_close)

    orange_coverage = next((coverage for coverage in all_coverage if coverage.operator == "Orange"), None)
    assert orange_coverage is not None
    assert orange_coverage.supports_2G == False
    assert orange_coverage.supports_3G == False
    assert orange_coverage.supports_4G == False
