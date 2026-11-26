import { describe, expect, it } from "vitest";
import { mount } from "@vue/test-utils";
import ConfirmDialog from "../components/ConfirmDialog.vue";

const make = () => mount(ConfirmDialog, { props: { open: true, title: "Delete?", text: "Sure?" }, attachTo: document.body });

describe("ConfirmDialog", () => {
  it("is labelled by its title and focuses Cancel", async () => {
    const w = make();
    await w.vm.$nextTick();
    await w.setProps({ open: false });
    await w.setProps({ open: true });
    await w.vm.$nextTick();
    const d = w.find('[role="dialog"]');
    expect(w.find(`#${d.attributes("aria-labelledby")}`).text()).toBe("Delete?");
    expect(document.activeElement.textContent).toBe("Cancel");
    w.unmount();
  });
  it("closes on Escape and traps Tab", async () => {
    const w = make();
    const d = w.find('[role="dialog"]');
    const [cancel, ok] = w.findAll("button");
    ok.element.focus();
    await d.trigger("keydown", { key: "Tab" });
    expect(document.activeElement).toBe(cancel.element);
    await d.trigger("keydown", { key: "Escape" });
    expect(w.emitted("cancel")).toHaveLength(1);
    w.unmount();
  });
});
