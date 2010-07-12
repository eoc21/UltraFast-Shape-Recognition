package eoc21.client;

import java.util.ArrayList;

import com.smartgwt.client.types.Autofit;
import com.smartgwt.client.types.Overflow;
import com.smartgwt.client.types.SelectionAppearance;
import com.smartgwt.client.types.TreeModelType;
import com.smartgwt.client.widgets.events.ScrolledHandler;
import com.smartgwt.client.widgets.layout.Layout;
import com.smartgwt.client.widgets.layout.SectionStack;
import com.smartgwt.client.widgets.layout.SectionStackSection;
import com.smartgwt.client.widgets.tree.Tree;
import com.smartgwt.client.widgets.tree.TreeGrid;
import com.smartgwt.client.widgets.tree.TreeNode;

/**
 * Gives information on the most recent things in my life.
 * @author ed
 *
 */
public class RecentUpdatesPanel {
	private SectionStack recentNewsSectionStack;
	private SectionStackSection news;
	private SectionStackSection events;

	
	public SectionStack setUpPanel(){
		recentNewsSectionStack = new SectionStack();
		recentNewsSectionStack.setWidth(250);
		recentNewsSectionStack.setHeight(250);
		setUpNewSection();
		setUpEventsSection();
		recentNewsSectionStack.addSection(news);
		recentNewsSectionStack.addSection(events);
		
		return recentNewsSectionStack;
	}
	
	private void setUpNewSection(){
		//Set up a tree with news updates.
		news = new SectionStackSection();
		news.setTitle("News");
		ArrayList<PartsTreeNode> newsNodes = new ArrayList<PartsTreeNode>();
		PartsTreeNode oeJob = new PartsTreeNode("openEye");
        oeJob.setAttribute("Name", "Job at OpenEye");
        newsNodes.add(oeJob);
		PartsTreeGrid treeGrid = setUpTreeGrid(newsNodes);
		news.addItem(treeGrid);
	}
	
	private void setUpEventsSection(){
		events = new SectionStackSection();
		events.setTitle("Events");
		events.setCanCollapse(true);
		events.setExpanded(true);
		ArrayList<PartsTreeNode> eventNodes = new ArrayList<PartsTreeNode>();
        PartsTreeNode acsBoston2010 = new PartsTreeNode("ACSBoston"); 
        acsBoston2010.setAttribute("Name", "Presenting a poster at the 2010 Boston ACS");
        eventNodes.add(acsBoston2010);
		PartsTreeGrid treeGrid = setUpTreeGrid(eventNodes);
		Layout treeLayout = new Layout();
		treeLayout.setOverflow(Overflow.AUTO);
		treeGrid.setFixedFieldWidths(false);
		treeLayout.addChild(treeGrid);
		events.addItem(treeGrid);
	}
	
	private PartsTreeGrid setUpTreeGrid(ArrayList<PartsTreeNode>nodes){
		PartsTreeGrid newsTreeGrid = new PartsTreeGrid();
		newsTreeGrid.setFolderIcon("100px-OpenEye_logo.jpg");
		newsTreeGrid.setNodeIcon("100px-OpenEye_logo.jpg");
		Tree grid1Tree = new Tree();
        grid1Tree.setModelType(TreeModelType.CHILDREN);
        PartsTreeNode news = new PartsTreeNode("Information");
        grid1Tree.setNameProperty("Name");
        news.setAttribute("Name", "Root");
        grid1Tree.setRoot(news);
        for(PartsTreeNode n: nodes){
        	grid1Tree.add(n, news);
        }
        newsTreeGrid.setData(grid1Tree);
		return newsTreeGrid;
	}
	 public static class PartsTreeGrid extends TreeGrid {
         public PartsTreeGrid() {
                 setWidth(250);
                 setHeight(250);
                 setShowEdges(true);
                 setBorder("0px");
                 setBodyStyleName("normal");
                 setAlternateRecordStyles(true);
                 setShowHeader(false);
                 setLeaveScrollbarGap(false);
                 setManyItemsImage("100px-OpenEye_logo.jpg");
             //    setAppImgDir("pieces/16/");
                 setCanReorderRecords(true);
                 setCanAcceptDroppedRecords(false);
                 setCanDragRecordsOut(true);
                 setAddDropValues(true);
                 this.setAutoFitData(Autofit.BOTH);
                 setSelectionAppearance(SelectionAppearance.CHECKBOX);
         }
 }


 public static class PartsTreeNode extends TreeNode {
         public PartsTreeNode(final String name, final String icon) {
                 this(name, icon, new PartsTreeNode[] {});
         }

         public PartsTreeNode(final String name, PartsTreeNode... children) {
                 this(name, null, children);
         }

         public PartsTreeNode(final String name, final String icon,
                         PartsTreeNode... children) {
                 setAttribute("Name", name);
                 setAttribute("children", children);
                 if (icon != null)
                         setAttribute("icon", icon);

         }
 }

}
