<template>
  <div
    :style="{ top: (position.y) + 'px', right: '50px' }"
    class="screen-templates-tooltip"
  >
    <slot
      name="screen-templates-tooltip-body"
    />
  </div>
</template>

<script>
export default {
  props: {
    position: {
      type: Object,
      default: () => {},
    },
  },
};
</script>

<style scoped>
.screen-templates-tooltip {
  position: absolute;
  border-radius: 4px;
  height: 45px;
  background-color: #FFFFFF;
  color: #566877;
  padding: 2px 8px 0 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
