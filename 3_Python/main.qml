import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtQml 2.15
import QtWebEngine 1.10
import io.integrals.LoaderManager 1.0



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
                visible: loaderManager.frame_now != "topic.qml"
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
        width: 0.33 * appWindow.width
        height: appWindow.height
        interactive: loaderManager.nav_visibility && loaderManager.frame_now != "topic.qml"

        Label {
            text: "Content goes here!"
            anchors.centerIn: parent

        }
    }

    Loader{
        property string url
        anchors.fill: parent
        anchors.centerIn: parent
        objectName: "pageLoader"
        id: pageLoader
        // source: loaderManager.frame_now
        source: "generator.qml"
    }

}
