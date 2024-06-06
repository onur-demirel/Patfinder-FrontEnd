<template>
  <PrimeDialog
    :visible="visible"
    :abstract="abstract"
    modal
    header="Details"
    :style="{ width: '25rem' }"
    @hide="onClose()"
    close-on-escape= "close-on-escape"
    @update:visible="onClose()"
  >
    <div>
      <p>{{ abstract }}</p>
    </div>


  </PrimeDialog>
</template>

<script>

export default {
  components: {},
  data() {
    return {};
  },

  computed: {},

  methods: {
    onClose() {
      //console.log("Tried to close with onClose");
      this.$emit("close");
      this.$emit("update:visible", false);
    },
  },

  props: {
    visible: Boolean,
    abstract: String,
    // abstract: String, //caused errors for now
  },
  emits: ["update:visible", "close"],
};
</script>
