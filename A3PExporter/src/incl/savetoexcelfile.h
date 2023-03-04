#ifndef SAVETOEXCELFILE_H
#define SAVETOEXCELFILE_H

#include "../QXlsx/header/xlsxworkbook.h"
#include "../QXlsx/header/xlsxdocument.h"
#include "../QXlsx/header/xlsxformat.h"
#include <QFileDialog>
#include <QTableView>

bool saveToExcelFile(QTableView *view, const QString &fname = QString());

#endif // SAVETOEXCELFILE_H
