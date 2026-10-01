import QtQuick
import Quickshell
import Quickshell.Io
import qs.Ui
import qs.Commons

BarWidget {
  id: root
  moduleName: "io.github.nwohater.sysmon"

  readonly property string scriptPath:
    Qt.resolvedUrl("sysmon-stats").toString().replace(/^file:\/\//, "")

  property real cpuPct: 0
  property real memPct: 0
  property real diskPct: 0
  readonly property bool warn: cpuPct >= 80 || memPct >= 80 || diskPct >= 90

  function refresh() {
    if (statsProc.running) return
    statsProc.running = true
  }

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  Process {
    id: statsProc
    command: ["bash", root.scriptPath]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        try {
          var data = JSON.parse(text || "{}")
          root.cpuPct = Number(data.cpu) || 0
          root.memPct = Number(data.mem) || 0
          root.diskPct = Number(data.disk) || 0
        } catch (e) {
          return
        }
      }
    }
  }

  // A 0.3s sample lives inside each run of sysmon-stats, so a 2s interval
  // keeps the number moving without spawning the sampler back to back.
  Timer {
    interval: 2000
    running: true
    repeat: true
    triggeredOnStart: true
    onTriggered: root.refresh()
  }

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: "CPU " + Math.round(root.cpuPct) + "%  MEM " + Math.round(root.memPct) + "%"
    fontSize: Style.font.body
    horizontalMargin: 6
    active: root.warn
    tooltipText: "CPU usage: " + Math.round(root.cpuPct) + "%\nMemory usage: " + Math.round(root.memPct) + "%\nDisk usage (/): " + Math.round(root.diskPct) + "%\nClick to open btop"
    onPressed: root.bar.run("omarchy-launch-floating-terminal-with-presentation btop")
  }
}
