import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtQml 2.15
import QtWebEngine 1.10
import QtGraphicalEffects 1.0
import io.integrals.LoaderManager 1.0
import "models"



ApplicationWindow {
    id: appWindow
    // flags: Qt.FramelessWindowHint
    minimumWidth: 700
    minimumHeight: 500
    width: 1000
    height: 633
    visible: true
    Material.theme: Material.System
    Material.primary: "#9499B7"
    Material.background: "#C5CAE9"
    title: qsTr("integrals.pank.su")
    Component.onCompleted: {
        WebEngine.settings.pluginsEnabled = true
        WebEngine.settings.javascriptEnabled = true
        // WebEngine.settings.showScrollBars = false
        WebEngine.settings.allowRunningInsecureContent = true
        WebEngine.defaultProfile.persistentCookiesPolicy = WebEngineProfile.AllowPersistentCookies
    }

    LoaderManager{
        id: loaderManager
    }

    header: ToolBar {
        id: toolbar
        Material.foreground: "#ffffff"
        visible: loaderManager.nav_visibility
        RowLayout {
            anchors.fill: parent
            ToolButton {
                icon.source: "qrc:/drawable/nav_btn.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now != "topic.qml" && loaderManager.mode != "Offline"
                onClicked:{
                    drawer.visible = true
                }
            }
            ToolButton {
                icon.source: "qrc:/drawable/navigate_next.svg"
                icon.color: "#ffffff"
                visible: loaderManager.frame_now == "topic.qml"
                onClicked:{
                    loaderManager.frame_now = "topics.qml"
                    loaderManager.header = "Темы"
                }
            }
            Label {
                text: loaderManager.header
                font.pixelSize: 32
                horizontalAlignment: Qt.AlignHCenter
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
                Layout.rightMargin: 44
            }
        }
    }
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