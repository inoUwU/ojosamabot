package main

import (
	"C"
	"github.com/jiro4989/ojosama"
	"log"
	"math/rand"
	"time"
)

func main() {
}

//export convertOjosama
func convertOjosama(t *C.char) *C.char {
	rand.Seed(time.Now().UnixNano())
	text := C.GoString(t)

	text, err := ojosama.Convert(text, nil)
	if err != nil {
		log.Println(err)
	}
	return C.CString(text)
}
