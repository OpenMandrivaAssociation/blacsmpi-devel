%define name	blacsmpi-devel	
%define	version 1.1
%define release	%mkrel 11
%define lib_name_orig lib%{name}
%define lib_major 0
%define lib_name %{lib_name_orig}%{lib_major}

Summary:	Blacsmpi Basic Linear Algebra Communication Subprograms
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.netlib.org/blacs/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-patch03.tar.bz2
Patch0: 	%name-Bmake.in.patch
# Tell it to use f95 instead of f77 due to gfortran changes
Patch1:		blacsmpi-devel-1.1-f95.patch
Requires:	mpich-devel
Provides:	%{name}-%{version}
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	mpich-devel 
BuildRequires:  gcc-gfortran

%description
The BLACS (Basic Linear Algebra Communication Subprograms) project
is an ongoing investigation whose purpose is to create a linear 
algebra oriented message passing interface that may be implemented 
efficiently and uniformly across a large range of distributed memory 
platforms.

%prep
rm -rf $RPM_BUILD_ROOT

%setup 
cd %{_builddir}
tar xvfj %{SOURCE1}

%patch0 -p 0
%patch1 -p0 -b .f95

%build

cp %{_builddir}/%{name}-%{version}/BMAKES/Bmake.MPI-LINUX %{_builddir}/%{name}-%{version}/Bmake.inc

make mpi

%install
mkdir -p %{buildroot}/%_libdir/%{name}-%{version}
mkdir -p %{buildroot}/%_includedir


cp LIB/blacsCinit_MPI-LINUX-0.a %{buildroot}/%_libdir/%{name}-%{version}/blacsCinit_MPI-LINUX-0.a
cp LIB/blacsF77init_MPI-LINUX-0.a %{buildroot}/%_libdir/%{name}-%{version}/blacsF77init_MPI-LINUX-0.a
cp LIB/blacs_MPI-LINUX-0.a %{buildroot}/%_libdir/%{name}-%{version}/blacs_MPI-LINUX-0.a
cp SRC/MPI/Bconfig.h %{buildroot}/%_includedir/Bconfig.h
cp SRC/MPI/Bdef.h %{buildroot}/%_includedir/Bdef.h

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root) 
%doc README
%{_libdir}/%{name}-%{version}/blacsCinit_MPI-LINUX-0.a
%{_libdir}/%{name}-%{version}/blacsF77init_MPI-LINUX-0.a
%{_libdir}/%{name}-%{version}/blacs_MPI-LINUX-0.a
%_includedir/Bdef.h
%_includedir/Bconfig.h
