#ifndef EXPORTER_H
#define EXPORTER_H

#include <QWidget>
#include <QFileSystemModel>
#include <QCompleter>
#include <QSharedMemory>
#include "corelthread.h"
#include "a3database.h"

QT_BEGIN_NAMESPACE
namespace Ui { class Exporter; }
QT_END_NAMESPACE

QT_BEGIN_NAMESPACE
namespace CustomClassNS {
    class FileSystemModel;
    class FSCompleter; }
QT_END_NAMESPACE

class CustomClassNS::FileSystemModel : public QFileSystemModel
{
public:
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
};

class CustomClassNS::FSCompleter : public QCompleter
{
public:
    QString pathFromIndex(const QModelIndex &idx) const override;
};

class Exporter : public QWidget
{
    Q_OBJECT
    QSharedMemory *qsm;
    QSettings *glb;
public:
    Exporter(QWidget *parent = nullptr);
    ~Exporter();

public slots:
    void handleCorelResult(const QMap<QString, QVariant> &res);
    void handleExportResult(const QMap<QString, QVariant> &res);
    const QString currentExportFolder();
    const bool &isFirstInstance() const {return firstInstance;}

private slots:
    QString pickExportFolder(const QString &currentDir);
    void on_tbDet_clicked();
    void updateQty();
    void requestExport();
    void on_btPdfSetting_clicked();
    void on_saveData(const QString &p);
    void manageNavigasi();
    void on_pbFilter_clicked();
    void on_pbDetach_clicked();
    void updateExportFolder(const QString& name);
    void on_pushButton_clicked();
    void comboVersiChanged(int index);

private:
    void toggleExportButton();
    void disablesAll();
    void enablesAll();
    void tableContextMenu(const QPoint &pos);
    bool firstInstance;
    A3DataBase db;
    Ui::Exporter *ui;
    CorelThread corel;
    QString exportName;

signals:
    void exportFolderChanged(const QString &c);
    void saveData(const QString &s);
};
#endif // EXPORTER_H
