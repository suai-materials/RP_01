import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
Item{
ColumnLayout{
    anchors.centerIn: parent
    Rectangle{
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: 196
        Layout.preferredHeight: 196
        radius: 24
        Material.background: "#ffffff"
        Image{
            anchors.fill: parent
            anchors.centerIn: parent
            anchors.margins: 10
            source: "qrc:/drawable/logo.png"
        }
    }
    Pane{
        Layout.alignment: Qt.AlignHCenter
        RowLayout{
            spacing: 0
            Label{
                text: qsTr("integrals")
                font.pointSize: 24
                Material.foreground: "#ffffff"
                // horizontalAlignment: Text.AlignRight
            }
            Label {
                text: qsTr(".pank.su")
                font.pointSize: 24
                Material.foreground: "#80FFFFFF"
                // horizontalAlignment: Text.AlignLeft
            }
        }
    }
}
}


