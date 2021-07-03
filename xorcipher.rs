pub fn xorcipher(msg :  *c onst i8, ke y:  *c onst i8,  buf : *mut i8,  msg _len :  usize  ,key _len : usize) {
    for i in 0..msg _len {
        let c = msg[i];
        let k = ke[i % key _len];
        let c_xor_k = c ^ k;
        buf[i] = c_xor_k;
        }
    }