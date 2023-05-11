# Releases and version numbers

These describe some of our practices and principles for making releases.

## Release strategy

Here are guiding principles for making releases:

**Release early and often**.
If it has been more than a few weeks since the last release, anybody is encouraged to make a new one.
Releases should be as painless and automated as possible.

**Roughly follow semver**.
See [our SemVer guide](releases:semver) for interpretation of what this means.

**We can always make another release**.
Don't try to get everything perfect before a release.
Favor making more releases more quickly rather than fewer bigger releases.

(releases:semver)=
## Version numbers

This theme roughly follows the [SemVer](https://semver.org) versioning scheme.
This corresponds to:

- **Major versions**: Significant refactoring of theme structure or functionality that requires major re-configurations for users and developers.
- **Minor versions**: Most enhancements and tweaks to theme behavior.
  This is the majority of version bumps.
- **Patch versions**: Tiny bugfixes and very minor improvements that trigger a release right when they are implemented.

Here are some guiding principles for version numbering:

**Do not worry about it too much**.
Don't take too much energy in deciding and debating versions.
Life is too short to worry about getting the perfect version number, just go with your gut (or ask another person if you really wish).

**It is more important to document a breaking change properly**.
When we make breaking changes, the important thing is to properly document them and create deprecation warnings and pathways.
This should get more energy than deciding whether to bump the major/minor version.

**Major version bumps should be for truly major overhauls**.
We're likely be breaking things here and there throughout, not every single breaking change.
Reserve major version changes for significant overhauls (for example, ones that require someone to comprehensively re-work thier CSS rules).

**Major versions do not have any special meaning other than semver**.
While we generally try not to bump major versions, they also carry no special meaning other than reflecting how much changed since the last version.
We try to follow [SemVer](https://semver.org) and this is all that major versions signify.
We don't make any promises about long term support and stability.
