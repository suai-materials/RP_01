import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtWebEngine 1.10

ColumnLayout{
    Rectangle{
        Layout.alignment: Qt.AlignHCenter
        width: 400
        height: 225
        color: "#FFF7FF"
        radius: 24
        WebEngineView{
            // anchors.fill: parent
            anchors.centerIn: parent
            url: "https://integrals.pank.su"
        }
    }
    Row{
        Layout.alignment: Qt.AlignHCenter
        Rectangle{
            width: 237
            height: 56
            color: "#FFF7FF"
            radius: 12
            Text{
                anchors.centerIn: parent
                text: "Ваш ответ:"
                font.family: "Roboto"
                font.pixelSize: 36
                color: "#9499B7"
                font.weight: Font.Medium
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
        TextArea {
            width: 130
            height: 56
        }
    }

}