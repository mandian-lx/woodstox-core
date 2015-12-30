%{?_javapackages_macros:%_javapackages_macros}
%global base_name woodstox
%global core_name %{base_name}-core
%global stax2_ver  3.1.1

Name:           %{core_name}
Version:        4.2.0
Release:        2.2
Summary:        High-performance XML processor
Group:		Development/Java
License:        ASL 2.0 or LGPLv2+ or BSD
URL:            http://%{base_name}.codehaus.org/
BuildArch:      noarch

Source0:        http://%{base_name}.codehaus.org/%{version}/%{core_name}-src-%{version}.tar.gz
Patch0:         %{name}-stax2-api.patch

BuildRequires:  maven-local
BuildRequires:  mvn(javax.xml.stream:stax-api)
BuildRequires:  mvn(net.java.dev.msv:msv-core)
BuildRequires:  mvn(net.java.dev.msv:xsdlib)
BuildRequires:  mvn(org.apache.felix:org.osgi.core)
BuildRequires:  mvn(org.codehaus.woodstox:stax2-api)
# Transitive devel dependencies needed because some packages don't
# install effective POMs:
BuildRequires:  mvn(net.java:jvnet-parent:pom:)

%description
Woodstox is a high-performance validating namespace-aware StAX-compliant
(JSR-173) Open Source XML-processor written in Java.
XML processor means that it handles both input (== parsing)
and output (== writing, serialization)), as well as supporting tasks
such as validation.

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{base_name}-%{version}
%patch0

# Create POM from template
sed s/@VERSION@/%{version}/\;s/@REQ_STAX2_VERSION@/%{stax2_ver}/ \
    src/maven/%{name}-asl.pom >pom.xml

# Remove bundled libraries.
rm -rf lib
rm -rf src/maven
rm -rf src/resources
rm -rf src/samples
rm -rf src/java/org
rm -rf src/test/org
rm -rf src/test/stax2

# Bundled libraries were removed, so dependencies on them need to be
# added.
%pom_add_dep net.java.dev.msv:msv-core
%pom_add_dep org.apache.felix:org.osgi.core
%pom_add_dep net.java.dev.msv:xsdlib

# Upstream uses non-standard directory structure.
%pom_xpath_inject pom:project "
    <build>
      <sourceDirectory>src/java</sourceDirectory>
      <testSourceDirectory>src/test</testSourceDirectory>
    </build>"

%mvn_alias ":{woodstox-core}-asl" :@1-lgpl
%mvn_file : %{name}{,-asl,-lgpl}

%build
# stax2 missing -> cannot compile tests -> tests skipped
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc release-notes

%files javadoc -f .mfiles-javadoc
%doc release-notes/asl release-notes/lgpl release-notes/bsd

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-1
- Update to upstream version 4.2.0

* Thu Jun 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.1.2-6
- Install NOTICE file with javadoc package
- Update to current packaging guidelines

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.1.2-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Jaromir Capik <jcapik@redhat.com> - 4.1.2-1
- Initial version
