exports.cmd = 'emcc -Os src/app/wasm/3d-model/3d-model.c -o src/assets/wasm/3d-model.js -s LEGACY_GL_EMULATION=1 -s EXTRA_EXPORTED_RUNTIME_METHODS="[\'ccall\']"';
