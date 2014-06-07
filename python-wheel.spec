# Created by pyp2rpm-1.0.1
%global pypi_name wheel

Name:           python35-%{pypi_name}
Version:        0.22.0
Release:        3%{?dist}
Summary:        A built-package format for Python

License:        MIT
URL:            http://bitbucket.org/dholth/wheel/
Source0:        https://pypi.python.org/packages/source/w/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Some test files are not present in tarball, so we include them separately.
# Upstream pull request to include the files in tarball:
# https://bitbucket.org/dholth/wheel/pull-request/34 (Patch0 below)
# (version 0.22 doesn't have a tag, so we're using commit hash to point to the
#  correct testing wheel)
Source1:        https://bitbucket.org/dholth/wheel/src/099352e/wheel/test/test-1.0-py2.py3-none-win32.whl
Source2:        https://bitbucket.org/dholth/wheel/raw/099352e/wheel/test/pydist-schema.json
Patch0:         wheel-0.22-add-test-files-to-manifest.path
Patch1:         wheel-0.22-legacy-keyring-compatibility.patch
Patch2:         wheel-0.22-fix-tests-broken-by-keyring-fix.patch
BuildArch:      noarch
 
BuildRequires:  python35-devel
BuildRequires:  python35-setuptools

%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

This is package contains Python 3 version of the package.

%prep
%setup -q -n %{pypi_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

# copy test files in place
cp %{SOURCE1} %{pypi_name}/test/
cp %{SOURCE2} %{pypi_name}/test/
# header files just has to be there, even empty
touch %{pypi_name}/test/headers.dist/header.h

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py


%build
%{__python35} setup.py build


%install
%{__python35} setup.py install --skip-build --root %{buildroot}

pushd %{buildroot}%{_bindir}
for f in $(ls); do mv $f python35-$f; done
popd


%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/python35-egg2wheel
%{_bindir}/python35-wheel
%{_bindir}/python35-wininst2wheel
%{python35_sitelib}/%{pypi_name}*
%exclude %{python35_sitelib}/%{pypi_name}/test


%changelog
* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-3
- Another rebuild with python 3.4

* Fri Apr 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-2
- Rebuild with python 3.4

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.
