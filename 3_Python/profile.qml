import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.0

Item{
    ProfileManager{
        id: profileManager
        token: loaderManager.get_token()
    }
    Rectangle {
        height: parent.height
        width: 264
        ColumnLayout{
            anchors.top: parent.top
            Image {
                id: img
                Layout.margins: 20
                source: loaderManager.get_photo_url()
                Layout.preferredWidth: 224
                Layout.preferredHeight: 224
                fillMode: Image.PreserveAspectCrop
                layer.enabled: true
                layer.effect: OpacityMask {
                    maskSource: mask
                }
            }

            Rectangle {
                id: mask
                width: 224
                height: 224
                radius: 250
                visible: false
            }

            Text{
                id: first_name
                text: profileManager.get_first_name()
                color: "#000000"
                font.family: "Roboto"
                font.pixelSize: 20
            }
            Text{
                id: last_name
                text: profileManager.get_last_name()
                color: "#000000"
                font.family: "Roboto"
                font.pixelSize: 20
            }

        }
    }
    Rectangle {
        height: parent.height
        anchors.right: parent.right
        width: parent.width - 264
        color: "#FFF7FF"
        ColumnLayout{
            anchors.top: parent.top
            anchors.topMargin: 20
            Text{
                text: "Ваш средний балл: " + profileManager.get_avarage_grade()
                font.family: "Roboto"
                font.pixelSize: 20
            }
            Text{
                text: "Процент выполненых заданий в генераторе: " + Math.floor(profileManager.get_generator_percent() * 100) + "%"
                font.family: "Roboto"
                font.pixelSize: 20
            }
        }
    }
}