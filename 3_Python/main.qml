import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtQml 2.15
import QtWebEngine 1.10
import QtGraphicalEffects 1.0
import QtQuick.Dialogs 1.3
import io.integrals.api 1.0
import "models"


ApplicationWindow {
    id: appWindow
    minimumWidth: 700
    minimumHeight: 500
    width: 1000
    height: 633
    visible: true
    Material.theme: Material.System
    Material.accent: "#D1C4E9"
    Material.primary: "#9499B7"
    Material.background: "#C5CAE9"
    title: qsTr("integrals.pank.su")
    Component.onCompleted: {
        // Настройка WebEngine
        WebEngine.settings.pluginsEnabled = true
        WebEngine.settings.javascriptEnabled = true
        WebEngine.settings.allowRunningInsecureContent = true
        WebEngine.defaultProfile.persistentCookiesPolicy = WebEngineProfile.AllowPersistentCookies
    }
    // Диалог, который показывается, когда выходишь из теста
    Dialog{
        id: questionDialog
        title: "Вы уверены?"
        standardButtons: StandardButton.Yes | StandardButton.No
        Text{
            anchors.centerIn: parent
            text: "Вы уверены, что вы хотите выйти из теста? \n Данные не будут отправлены и попытка будет потрачена."
        }
        onYes:{
            loaderManager.close_test()
            loaderManager.frame_now = "tests.qml"
        }
    }

    // тип созданны в Питоне
    LoaderManager{
        id: loaderManager
    }

    // Заголовок страницы
    header: ToolBar {
        id: toolbar
        Material.foreground: "#ffffff"
        visible: loaderManager.nav_visibility
        RowLayout {
            anchors.fill: parent
            /* Кнопки которые можно объединить в две, но ради понятности что делает
            какая кнопка и когда она показыватся, они разделены */
            // Кнопка навиации
            ToolButton {
                icon.source: "qrc:/drawable/nav_btn.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now != "webpage.qml" && loaderManager.mode != "Offline"
                onClicked:{
                    drawer.visible = true
                }
            }
            // Кнопка возвращения из темы в список тем
            ToolButton {
                icon.source: "qrc:/drawable/navigate_next.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now == "webpage.qml" && loaderManager.webpage_mode == "Topic"
                onClicked:{
                    loaderManager.frame_now = "topics.qml"
                    loaderManager.header = "Темы"
                    loaderManager.webpage_mode = "NotShowing"
                }
            }
            Label {
                text: loaderManager.header
                font.pixelSize: 32
                anchors.centerIn: parent
            }
            // Кнопка перезагрузки приложения, например для смены аккаунта или выхода из офлайн режима
            ToolButton {
                Layout.alignment: Qt.AlignRight
                icon.source: "qrc:/drawable/exit_icon.svg"
                icon.color: "#ffffff"
                visible: loaderManager.mode == "Offline" || loaderManager.frame_now == "profile.qml"
                onClicked:{
                    loaderManager.reload()
                }
            }

            // Кнопка обновления примера а генераторе
            ToolButton {
                Layout.alignment: Qt.AlignRight
                icon.source: "qrc:/drawable/reload_icon.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now == "generator.qml"
                onClicked:{
                    loaderManager.frame_now = ""
                    loaderManager.frame_now = "generator.qml"
                }
            }
            // Кнопкаа закрытия теста
            ToolButton {
                Layout.alignment: Qt.AlignRight
                icon.source: "qrc:/drawable/close_icon.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now == "webpage.qml" && loaderManager.webpage_mode == "Test"
                onClicked:{
                    questionDialog.open()
                }
            }
            // Кнопкаа закрытия результатов теста
            ToolButton {
                Layout.alignment: Qt.AlignRight
                icon.source: "qrc:/drawable/close_icon.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now == "webpage.qml" && loaderManager.webpage_mode == "TestResult"
                onClicked:{
                    loadderManager.frame_now = "tests.qml"
                }
            }
        }
    }
    // Панель навигации
    Drawer {
        id: drawer
        width: 325
        height: appWindow.height
        interactive: (loaderManager.nav_visibility && loaderManager.frame_now != "topic.qml") && loaderManager.mode != "Offline"
        ListView{
            id: listView
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.topMargin: 20
            contentWidth: parent.width - 20
            spacing: 50
            model: NavigationModel {}
            delegate:
            Item{
                Rectangle{
                    id: rect
                    width: listView.contentWidth
                    height: 40
                    radius: 44
                    color: to_navigate === loaderManager.frame_now ? "#FFF7FF" : "#A094B7"
                    Row{
                        anchors.fill: parent
                        Image{
                            id: icon
                            height: parent.height * 0.8
                            width: height
                            source: logo
                            visible: false
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.leftMargin: 10
                        }
                        ColorOverlay{
                            anchors.fill: icon
                            source: icon
                            color: to_navigate === loaderManager.frame_now ? "#9499B7" : "#F8FDFF"
                            antialiasing: true
                            visible: true
                        }
                        Text{
                            text: name
                            height: parent.height
                            color: to_navigate === loaderManager.frame_now ? "#9499B7" : "#F8FDFF"
                            font.family: "Roboto"
                            font.pixelSize: 20
                            font.weight: Font.Medium
                            verticalAlignment: Text.AlignVCenter
                            anchors.horizontalCenter: parent.horizontalCenter

                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            loaderManager.frame_now = to_navigate
                            loaderManager.header = name
                        }
                    }
                }
            }
        }
    }
    // Переключатель фреймов, зависит от LoaderManager
    Loader{
        property string url
        anchors.fill: parent
        anchors.centerIn: parent
        objectName: "pageLoader"
        id: pageLoader
        source: loaderManager.frame_now
        // source: "generator.qml"
    }

}
