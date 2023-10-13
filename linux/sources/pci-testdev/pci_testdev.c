#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/pci.h>
#include <linux/init.h>
#include <linux/pci_regs.h>

#define PCI_DEVICE_ID_REDHAT_TEST        0x0005

static struct pci_device_id ids[] = {
	{ PCI_DEVICE(PCI_VENDOR_ID_REDHAT, PCI_DEVICE_ID_REDHAT_TEST), },
	{ 0, }
};
MODULE_DEVICE_TABLE(pci, ids);

static unsigned char skel_get_revision(struct pci_dev *dev)
{
	u8 revision;

	pci_read_config_byte(dev, PCI_REVISION_ID, &revision);
	return revision;
}

static inline int check_pci_config(struct pci_dev *dev)
{
	u8 pin, line;
	u16 vendor, device;
	pci_read_config_byte(dev, PCI_INTERRUPT_PIN, &pin);
	pci_read_config_byte(dev, PCI_INTERRUPT_LINE, &line);
	dev_info(&dev->dev, "pin: %d, line: %d\n", pin, line);

	pci_read_config_word(dev, PCI_SUBSYSTEM_VENDOR_ID, &vendor);
	pci_read_config_word(dev, PCI_SUBSYSTEM_ID, &device);
	dev_info(&dev->dev, "vendor: 0x%x, device: 0x%x\n", vendor, device);

	return 0;
}

static int probe(struct pci_dev *dev, const struct pci_device_id *id)
{
	/* Do probing type stuff here.  
	 * Like calling request_region();
	 */
	if(pci_enable_device(dev)) {
		dev_err(&dev->dev, "can't enable PCI device\n");
		return -ENODEV;
	}
	
	if (skel_get_revision(dev) == 0x42)
		return -ENODEV;

	dev_info(&dev->dev, "class id: 0x%x\n", dev->class);
	check_pci_config(dev);

	return 0;
}

static void remove(struct pci_dev *dev)
{
	/* clean up any allocated resources and stuff here.
	 * like call release_region();
	 */
}

static struct pci_driver pci_driver = {
	.name = "pci_testdev",
	.id_table = ids,
	.probe = probe,
	.remove = remove,
};

static int __init pci_skel_init(void)
{
	return pci_register_driver(&pci_driver);
}

static void __exit pci_skel_exit(void)
{
	pci_unregister_driver(&pci_driver);
}

MODULE_LICENSE("GPL");

module_init(pci_skel_init);
module_exit(pci_skel_exit);
