#ifndef PARTICIPANTWIDGET_H
#define PARTICIPANTWIDGET_H

#include <QWidget>
#include <QTableWidgetItem>
#include <QListWidgetItem>

#include "DataEditorWidget.h"
#include "GlobalMessageBox.h"

#include "TeraSessionStatus.h"

namespace Ui {
class ParticipantWidget;
}

class ParticipantWidget : public DataEditorWidget
{
    Q_OBJECT

public:
    explicit ParticipantWidget(ComManager* comMan, const TeraData* data = nullptr, QWidget *parent = nullptr);
    ~ParticipantWidget();

    void saveData(bool signal=true);

    void connectSignals();

private:
    Ui::ParticipantWidget *ui;

    QMap<int, QTableWidgetItem*>    m_listSessions_items;
    QMap<int, TeraData*>            m_ids_session_types;
    QMap<int, TeraData*>            m_ids_sessions;

    QDialog*                     m_diag_editor;

    void updateControlsState();
    void updateFieldsValue();

    bool validateData();

    void updateSession(TeraData *session);
    void updateDevice(TeraData* device);

    void updateCalendars(QDate left_date);
    QDate getMinimumSessionDate();
private slots:
    void processFormsReply(QString form_type, QString data);
    void processSessionsReply(QList<TeraData> sessions);
    void processSessionTypesReply(QList<TeraData> session_types);
    void processDevicesReply(QList<TeraData> devices);
    void deleteDataReply(QString path, int id);

    void btnSave_clicked();
    void btnUndo_clicked();
    void btnDevices_clicked();
    void btnDeleteSession_clicked();

    void currentSelectedSessionChanged(QTableWidgetItem* current, QTableWidgetItem* previous);
    void displaySessionDetails(QTableWidgetItem* session_item);
    void currentTypeFiltersChanged(QListWidgetItem* changed);
    void displayNextMonth();
    void displayPreviousMonth();
};

#endif // PARTICIPANTWIDGET_H
