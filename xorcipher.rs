// takes two strings and returns the XOR of them
#[no_mangle]
pub fn cipher(msg :  *const i8, key:  *const i8,  buf : *mut i8,  msg_len :  usize  ,key_len : usize) {
    unsafe {
        for i in 0..msg_len {
                    let x = *msg.add(i);
                    let y = *key.add(i % key_len);
                    let z = x ^ y;
                    *buf.add(i) = z;
            }
    }
    
}
