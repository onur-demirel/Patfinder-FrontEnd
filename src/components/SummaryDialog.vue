<template>
  <PrimeDialog
    :visible="visible"
    :summary="summary"
    modal
    header="Summary"
    :style="{ width: '25rem' }"
    @hide="onClose()"
    close-on-escape= "close-on-escape"
    @update:visible="onClose()"
  >
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
    summary: String,
    // isSummaryGenerating: Boolean,
    // abstract: String, //caused errors for now
  },
  emits: ["update:visible", "close"],
};
</script>
