package main

import (
        "fmt"
        "github.com/opencontainers/selinux/go-selinux/label"
)

// Mirroring the behavior found here:
// https://github.com/containers/podman/blob/8432ed7488e9c62738f9308fcc03f2ae9c2cd615/libpod/util_linux.go#L110-L129
func main() {
        path := "/home/rmanes/Downloads"
        _, mountLabel, err := label.InitLabels([]string{})
        if err != nil {
                fmt.Errorf("Error getting default labels: %w", err)
        }

        // Deprecated
        // https://github.com/opencontainers/selinux/blob/main/go-selinux/label/label.go#L61
        if err := label.ReleaseLabel(mountLabel); err != nil {
                fmt.Errorf("Error releasing label: %q, %w", mountLabel, err)
        }

        if err := label.Relabel(path, mountLabel, true); err != nil {
                fmt.Errorf("Error relabeling path %s with label %q: %w", path, mountLabel, err)
        }

        fmt.Printf("Completed path \"%s\" relabeling with label %q.", path, mountLabel)
}
