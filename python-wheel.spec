# Created by pyp2rpm-1.0.1
%global pypi_name wheel
%global with_python2 0
%global with_python3 1

%{?scl:%scl_package python-%{pypi_name}}
%{!?scl:%global pkg_name %{name}}
%{?scl:%global py3dir %{_builddir}/python3-%{name}-%{version}-%{release}}

Name:           %{?scl_prefix}python-%{pypi_name}
Version:        0.24.0
Release:        0.4.20140726hg1bbbd010558a%{?dist}
Summary:        A built-package format for Python

License:        MIT
URL:            http://bitbucket.org/dholth/wheel/
Source0:        python3-nightly-wheel-1bbbd010558a.tar

BuildArch:      noarch

%if %{?with_python2}
BuildRequires:  python-devel
BuildRequires:  python-setuptools

BuildRequires:  pytest
BuildRequires:  python-jsonschema
BuildRequires:  python-keyring
%endif # if with_python2

%if %{?with_python3}
BuildRequires:  %{?scl_prefix}python3-devel
BuildRequires:  %{?scl_prefix}python3-setuptools
%endif # if with_python3


%description
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

%if 0%{?with_python3}
%package -n     %{?scl_prefix}python3-%{pypi_name}
Summary:        A built-package format for Python

%description -n %{?scl_prefix}python3-%{pypi_name}
A built-package format for Python.

A wheel is a ZIP-format archive with a specially formatted filename and the
.whl extension. It is designed to contain all the files for a PEP 376
compatible install in a way that is very close to the on-disk format.

This is package contains Python 3 version of the package.
%endif # with_python3


%prep
%setup -q -n python3-nightly-%{pypi_name}

# header files just has to be there, even empty
touch %{pypi_name}/test/headers.dist/header.h

# remove unneeded shebangs
sed -ie '1d' %{pypi_name}/{egg2wheel,wininst2wheel}.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{?scl:scl enable %scl - << \EOF}
%if 0%{?with_python2}
%{__python2} setup.py build
%endif # with_python2

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3
%{?scl:EOF}

%install
%{?scl:scl enable %scl - << \EOF}
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
pushd %{buildroot}%{_bindir}
for f in $(ls); do mv $f python3-$f; done
popd
%endif # with_python3

%if 0%{?with_python2}
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif # with_python2
%{?scl:EOF}

%check
%{?scl:scl enable %scl - << \EOF}
%if 0%{?with_python2}
# remove setup.cfg that makes pytest require pytest-cov (unnecessary dep)
rm setup.cfg
py.test --ignore build
%endif # with_python2

# no test for Python 3, no python3-jsonschema yet
%if 0
pushd %{py3dir}
rm setup.cfg
py.test-%{python3_version} --ignore build
popd
%endif # with_python3
%{?scl:EOF}


%if 0%{?with_python2}
%files
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/egg2wheel
%{_bindir}/wheel
%{_bindir}/wininst2wheel
%{python_sitelib}/%{pypi_name}*
%exclude %{python_sitelib}/%{pypi_name}/test
%endif # with_python2


%if 0%{?with_python3}
%files -n %{?scl_prefix}python3-%{pypi_name}
%doc LICENSE.txt CHANGES.txt README.txt
%{_bindir}/python3-egg2wheel
%{_bindir}/python3-wheel
%{_bindir}/python3-wininst2wheel
%{python3_sitelib}/%{pypi_name}*
%exclude %{python3_sitelib}/%{pypi_name}/test
%endif # with_python3


%changelog
* Sat Jul 26 2014 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-0.4.20140726hg1bbbd010558a
- Update to hg: 1bbbd010558a

* Mon Jul 07 2014 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-0.3.20140707hg12bbac667b6c
- Update to hg: 12bbac667b6c

* Sat Jun 07 2014 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-0.2.20140607hg79e669d9f170
- Remove already merged patches
- SCL

* Sat Jun 07 2014 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-0.1.20140607hg79e669d9f170
- Update to hg: 79e669d9f170

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-3
- Another rebuild with python 3.4

* Fri Apr 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-2
- Rebuild with python 3.4

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.
