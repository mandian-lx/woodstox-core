%{?_javapackages_macros:%_javapackages_macros}

%global base_name woodstox
%global core_name %{base_name}-core

Name:           %{core_name}
Version:        5.0.3
Release:        2%{?dist}
Summary:        High-performance XML processor
License:        ASL 2.0 or LGPLv2+ or BSD
URL:            https://github.com/FasterXML/woodstox
BuildArch:      noarch

Source0:        https://github.com/FasterXML/%{base_name}/archive/%{name}-%{version}.tar.gz
Patch0:         0001-stax2-api.patch

BuildRequires:  maven-local
BuildRequires:  mvn(com.fasterxml:oss-parent:pom:)
BuildRequires:  mvn(javax.xml.stream:stax-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.java.dev.msv:msv-core)
BuildRequires:  mvn(net.java.dev.msv:msv-rngconverter)
BuildRequires:  mvn(net.java.dev.msv:xsdlib)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.felix:org.osgi.core)
BuildRequires:  mvn(org.codehaus.woodstox:stax2-api)

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
%setup -q -n %{base_name}-%{name}-%{version}

%patch0 -p1

%pom_xpath_inject 'pom:plugin[pom:artifactId="maven-bundle-plugin"]/pom:configuration' '
<instructions>
    <Export-Package>{local-packages}</Export-Package>
</instructions>'

%mvn_alias ":{woodstox-core}" :@1-lgpl :@1-asl :wstx-asl :wstx-lgpl \
    org.codehaus.woodstox:@1 org.codehaus.woodstox:@1-asl \
    org.codehaus.woodstox:@1-lgpl org.codehaus.woodstox:wstx-lgpl \
    org.codehaus.woodstox:wstx-asl
%mvn_file : %{name}{,-asl,-lgpl}

# Fails even when using online maven build
rm ./src/test/java/org/codehaus/stax/test/stream/TestNamespaces.java

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md

%files javadoc -f .mfiles-javadoc

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Michael Simacek <msimacek@redhat.com> - 5.0.3-1
- Update to upstream version 5.0.3

* Mon Jul 04 2016 Michael Simacek <msimacek@redhat.com> - 5.0.2-1
- Update to upstream version 5.0.2

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 28 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.1-1
- Update to upstream version 5.0.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Michael Simacek <msimacek@redhat.com> - 5.0.0-2
- Fix missing classes and aliases
- Enable tests

* Mon Mar 23 2015 Michael Simacek <msimacek@redhat.com> - 5.0.0-1
- Update to upstream version 5.0.0

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-6
- Remove build-requires on jvnet-parent

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Michal Srb <msrb@redhat.com> - 4.2.0-4
- Add aliases: ":wstx-asl" ":wstx-lgpl"

* Thu Oct  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.0-3
- Fix usage of %%mvn_alias

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
