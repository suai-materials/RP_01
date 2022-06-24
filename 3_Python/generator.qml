import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtWebEngine 1.10
import io.integrals.api 1.0


ColumnLayout{
    GeneratorManager{
        id: generatorManager
    }
    Rectangle{
        Layout.alignment: Qt.AlignHCenter
        width: 400
        height: 225
        color: "#FFF7FF"
        radius: 24
        WebEngineView{
            id: webView
            // anchors.fill: parent
            width: 350
            height: 205
            anchors.centerIn: parent
            url: generatorManager.generate(loaderManager.get_token())
        }
    }
    Text{
        id: result
        visible: false
        text: "Верно"
        anchors.horizontalCenter: parent.horizontalCenter
        font.capitalization: Font.MixedCase
        font.family: "Roboto"
        font.pixelSize: 36
        color: "#FFF7FF"
        font.weight: Font.Medium
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    RowLayout{
        anchors.horizontalCenter: parent.horizontalCenter
        Rectangle{
            id: label
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
        TextField  {
            id: answer
            anchors.verticalCenter: parent.verticalCenter
            placeholderText: "Ответ"
            inputMethodHints : Qt.ImhFormattedNumbersOnly
            font.family: "Roboto"
            font.pixelSize: 27
            validator: DoubleValidator {}
            color: "#9499B7"
            bottomPadding: 8
            background: Rectangle {
                implicitWidth: 129
                implicitHeight: 56
                color: "#FFFFFF"
                border.color: "#FFF7FF"
                border.width: 3
                radius: 12
            }
        }
        Button{
            id: send_result_btn
            background: Rectangle{
                implicitWidth: 56
                implicitHeight: 56
                radius: 12
                color: "#D1C4E9"
                border.color: "#FFF7FF"
                border.width: 5
            }
            icon.width: 42
            icon.height: 42
            icon.source: "qrc:/drawable/done_icon.svg"
            icon.color: "#ffffff"
            onClicked:{
                send_result_btn.visible = false
                answer.enabled = false
                result.text = generatorManager.check_answer(answer.text, loaderManager.get_token()) ? "Верно" : "Неверно"
                result.visible = true
            }
        }
    }

}