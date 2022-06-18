import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts
import QtWebEngine 1.10


ColumnLayout {
    Image{
        Layout.preferredWidth: 224
        Layout.preferredHeight: 213
        source: "qrc:/drawable/sticker.png"
    }
    WebView{
        url: "https://www.google.ru"
    }
}
