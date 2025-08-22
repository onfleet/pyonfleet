# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.0] - 2025-08-22
### Added
- Added Route Plans endpoint support

## [1.4.1] - 2023-05-27
### Added
- Added support for Worker's Route Delivery Manifest

## [1.4.0] - 2023-05-15
### Added
- Added property for adding custom headers to all requests

## [1.3.1] - 2022-07-06
### Security
- Update dependencies (`backoff` v2.1.2, `requests` v2.28.1)

## [1.3.0] - 2022-04-26
### Added
- Get all tasks in team
- Get all worker assigned tasks

## [1.2.1] - 2021-11-04
### Fixed
- Query parameter bug fix

## [1.2] - 2021-10-07
### Changed
- `Onfleet` now uses endpoints declared statically (#24)
- `endpoint.py` has been refactored accordingly
- `request.py` has been refactored accordingly
- `error.py` has been refactored
### Removed
- `Config` class
### Fixed
- Tweaks for READMEs' accuracy, consistency and readability

## [1.1.6] - 2021-08-17
### Added
- New module: `_meta.py`
### Changed
- In `setup.py`, reads version from the meta module
- Update .gitignore
### Fixed
- In `requests.py`, imports version from the meta module –no need for `pkg_resources` (#18)

## [1.1.5] - 2021-06-28
### Added
- Add POST and PUT support to Hubs endpoint
- Add `autoDispatch`
- Add `getWorkerEta`
- Add missing Metadata endpoints

## [1.1.4] - 2021-04-08
### Fixed
- Error cause handling when cause is missing

## [1.1.3] - 2021-03-08
### Added
- Error causes to `HttpError` class (#19)
### Changed
- Expand terminology for Admins API endpoint

## [1.1.2] - 2020-12-14
### Fixed
- Error message handling (#14)

## [1.1.1] - 2020-11-10
### Fixed
- Distribution wheel containing redundant files (kudos to @bbradshaw for noticing)

## ~~[1.1.0] - 2020-08-19 -~~ Yanked
### Changed
- Refactored config JSON file into a Python module
### Fixed
- Bug on PyPI wheel distribution
- Bug on config directory problem with backslash in Windows
- Bug on locating config directory in cloud instances
- Bug on locating config directory in packaged instances (i.e. Electron)

## ~~[1.0.2] - 2020-07-02 -~~ Yanked
### Added
- Rate limiter
### Fixed
- Bug on directories when using Windows environment (#10)
- Issues found on wheel distribution and some bug in locating directories

## [1.0.1] - 2019-05-22
### Added
- Initial release on PyPI

[Unreleased]: https://github.com/onfleet/pyonfleet/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/onfleet/pyonfleet/compare/v1.4.1...v1.5.0
[1.4.1]: https://github.com/onfleet/pyonfleet/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/onfleet/pyonfleet/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.com/onfleet/pyonfleet/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/onfleet/pyonfleet/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/onfleet/pyonfleet/compare/v1.2...v1.2.1
[1.2]: https://github.com/onfleet/pyonfleet/compare/v1.1.6...v1.2
[1.1.6]: https://github.com/onfleet/pyonfleet/compare/v1.1.5...v1.1.6
[1.1.5]: https://github.com/onfleet/pyonfleet/compare/v1.1.4...v1.1.5
[1.1.4]: https://github.com/onfleet/pyonfleet/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/onfleet/pyonfleet/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/onfleet/pyonfleet/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/onfleet/pyonfleet/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/onfleet/pyonfleet/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/onfleet/pyonfleet/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/onfleet/pyonfleet/releases/tag/v1.0.1
