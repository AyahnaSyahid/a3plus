QT       += core gui axcontainer sql

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++14

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src/a3database.cpp \
    src/a3previewdatadialog.cpp \
    src/corelmanager/corelmanager.cpp \
    src/corelthread.cpp \
    src/main.cpp \
    src/exporter.cpp \
    src/models.cpp \
    src/previewmodel.cpp \
    src/savetoexcelfile.cpp \
    src/tentangaplikasi.cpp

HEADERS += \
    src/corelmanager/incl/corelmanager.h \
    src/incl/a3database.h \
    src/incl/a3previewdatadialog.h \
    src/incl/corelthread.h \
    src/incl/exporter.h \
    src/incl/models.h \
    src/incl/previewmodel.h \
    src/incl/savetoexcelfile.h \
    src/static-libs/header/xlsxabstractooxmlfile.h \
    src/static-libs/header/xlsxabstractooxmlfile_p.h \
    src/static-libs/header/xlsxabstractsheet.h \
    src/static-libs/header/xlsxabstractsheet_p.h \
    src/static-libs/header/xlsxcell.h \
    src/static-libs/header/xlsxcell_p.h \
    src/static-libs/header/xlsxcellformula.h \
    src/static-libs/header/xlsxcellformula_p.h \
    src/static-libs/header/xlsxcelllocation.h \
    src/static-libs/header/xlsxcellrange.h \
    src/static-libs/header/xlsxcellreference.h \
    src/static-libs/header/xlsxchart.h \
    src/static-libs/header/xlsxchart_p.h \
    src/static-libs/header/xlsxchartsheet.h \
    src/static-libs/header/xlsxchartsheet_p.h \
    src/static-libs/header/xlsxcolor_p.h \
    src/static-libs/header/xlsxconditionalformatting.h \
    src/static-libs/header/xlsxconditionalformatting_p.h \
    src/static-libs/header/xlsxcontenttypes_p.h \
    src/static-libs/header/xlsxdatavalidation.h \
    src/static-libs/header/xlsxdatavalidation_p.h \
    src/static-libs/header/xlsxdatetype.h \
    src/static-libs/header/xlsxdocpropsapp_p.h \
    src/static-libs/header/xlsxdocpropscore_p.h \
    src/static-libs/header/xlsxdocument.h \
    src/static-libs/header/xlsxdocument_p.h \
    src/static-libs/header/xlsxdrawing_p.h \
    src/static-libs/header/xlsxdrawinganchor_p.h \
    src/static-libs/header/xlsxformat.h \
    src/static-libs/header/xlsxformat_p.h \
    src/static-libs/header/xlsxglobal.h \
    src/static-libs/header/xlsxmediafile_p.h \
    src/static-libs/header/xlsxnumformatparser_p.h \
    src/static-libs/header/xlsxrelationships_p.h \
    src/static-libs/header/xlsxrichstring.h \
    src/static-libs/header/xlsxrichstring_p.h \
    src/static-libs/header/xlsxsharedstrings_p.h \
    src/static-libs/header/xlsxsimpleooxmlfile_p.h \
    src/static-libs/header/xlsxstyles_p.h \
    src/static-libs/header/xlsxtheme_p.h \
    src/static-libs/header/xlsxutility_p.h \
    src/static-libs/header/xlsxworkbook.h \
    src/static-libs/header/xlsxworkbook_p.h \
    src/static-libs/header/xlsxworksheet.h \
    src/static-libs/header/xlsxworksheet_p.h \
    src/static-libs/header/xlsxzipreader_p.h \
    src/static-libs/header/xlsxzipwriter_p.h \
    src/incl/tentangaplikasi.h

FORMS += \
    src/ui/a3previewdatadialog.ui \
    src/ui/exporter.ui \
    src/ui/tentangaplikasi.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

DISTFILES += \
    static-libs/libQXlsx.a

win32:CONFIG(release, debug|release): LIBS += -L$$PWD/static-libs/ -lQXlsx
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/static-libs/ -lQXlsxd

VERSION = 1.0.0.2

INCLUDEPATH += $$PWD/static-libs
DEPENDPATH += $$PWD/static-libs

win32-g++:CONFIG(release, debug|release): PRE_TARGETDEPS += $$PWD/static-libs/libQXlsx.a
else:win32-g++:CONFIG(debug, debug|release): PRE_TARGETDEPS += $$PWD/static-libs/libQXlsxd.a
else:win32:!win32-g++:CONFIG(release, debug|release): PRE_TARGETDEPS += $$PWD/static-libs/QXlsx.lib
else:win32:!win32-g++:CONFIG(debug, debug|release): PRE_TARGETDEPS += $$PWD/static-libs/QXlsxd.lib

RESOURCES += \
    res.qrc

RC_ICONS = E.ico
